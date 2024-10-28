from fastapi import FastAPI, Depends, HTTPException, status
from fastapi import request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta, datetime
from jose import JWTError, jwt
import subprocess
import time
from .database import get_db, Base, engine
from .models import Usuario
from .schemas import UsuarioCreate, Token
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import os
# Crear la base de datos
Base.metadata.create_all(bind=engine)

# Configurar la aplicación FastAPI
app = FastAPI()

# Configurar CORS
origins = [
    "http://localhost:5173",  # Cambia el puerto si es necesario
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuración de seguridad
SECRET_KEY = "secretkey123456"  # Cambia esto en producción
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Función para crear un usuario por defecto
def crear_usuario_por_defecto(db: Session):
    usuario = db.query(Usuario).filter(Usuario.email == "admin@admin.com").first()
    if not usuario:
        hashed_password = pwd_context.hash("admin")
        admin_user = Usuario(nombre="admin", email="admin@admin.com", password=hashed_password)
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        print("Usuario admin@admin.com creado con éxito")
    else:
        print("El usuario admin@admin.com ya existe")

# Evento que se ejecuta cuando la aplicación se inicia
@app.on_event("startup")
def startup():
    db = next(get_db())  # Obtener la sesión de la base de datos
    crear_usuario_por_defecto(db)

# Ruta para crear un nuevo usuario
@app.post("/register/")
async def create_user(user: UsuarioCreate, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(user.password)
    db_user = Usuario(nombre=user.nombre, email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"msg": "User created successfully"}

# Función para autenticar usuario
def authenticate_user(db: Session, email: str, password: str):
    user = db.query(Usuario).filter(Usuario.email == email).first()
    if not user:
        return False
    if not pwd_context.verify(password, user.password):
        return False
    return user

# Función para crear un token de acceso
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Ruta para obtener el token
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Ruta para verificar el token
@app.get("/users/me")
async def read_users_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(Usuario).filter(Usuario.email == email).first()
    if user is None:
        raise credentials_exception
    return user

# Ruta para ejecutar main.py
@app.post("/analisis-datos")
def ejecutar_analisis_datos():
    try:
        # Ejecutar el main.py
        subprocess.run(["python", "D:/Taller de investigacion/scraping/CuscoTrends/scraping/Analisis_Data/main.py"], check=True)
        return {"message": "Análisis de datos (main.py) completado con éxito"}
    except subprocess.CalledProcessError as e:
        return {"error": str(e), "output": e.output}

# Ruta para ejecutar EDA.py
@app.post("/analisis-eda")
def ejecutar_analisis_eda():
    try:
        subprocess.run(["python", "D:/Taller de investigacion/scraping/CuscoTrends/scraping/Analisis_Data/EDA.py"], check=True)
        return {"message": "Análisis EDA (EDA.py) completado con éxito"}
    except subprocess.CalledProcessError as e:
        return {"error": str(e), "output": e.output}

# Ruta para ejecutar machine_learning.py
@app.post("/analisis-ml")
def ejecutar_analisis_ml():
    try:
        subprocess.run(["python", "D:/Taller de investigacion/scraping/CuscoTrends/scraping/Analisis_Data/machine_learning.py"], check=True)
        return {"message": "Análisis de machine learning (machine_learning.py) completado con éxito"}
    except subprocess.CalledProcessError as e:
        return {"error": str(e), "output": e.output}
    
@app.post("/scraping-tripadvisor")
def ejecutar_scraping_tripadvisor():
    try:
        # Ejecutar el tour_scraper.py
        subprocess.run(["python", "D:/Taller de investigacion/scraping/CuscoTrends/scraping/TripAdvisor/tour_scraper.py"], check=True)

        # Agregar un delay de 30 segundos antes de ejecutar el siguiente script
        time.sleep(30)
        
        # Ejecutar el datasetCV.py
        subprocess.run(["python", "D:/Taller de investigacion/scraping/CuscoTrends/scraping/TripAdvisor/datasetCV.py"], check=True)

        return {"message": "Scraping de TripAdvisor completado con éxito"}
    except subprocess.CalledProcessError as e:
        return {"error": str(e), "output": e.output}
    
# Ruta para ejecutar Trustpilot secuencialmente
@app.post("/scraping-trustpilot")
def ejecutar_scraping_trustpilot():
    try:
        # Ejecutar extract_links.py primero
        subprocess.run(["python", "D:/Taller de investigacion/scraping/CuscoTrends/scraping/Trustpilot/extract_links.py"], check=True)

        # Retardo de 30 segundos antes de ejecutar el siguiente script
        time.sleep(30)

        # Ejecutar datasetCV.py después del retraso
        subprocess.run(["python", "D:/Taller de investigacion/scraping/CuscoTrends/scraping/Trustpilot/datasetCV.py"], check=True)

        return {"message": "Scraping de Trustpilot completado con éxito"}
    except subprocess.CalledProcessError as e:
        return {"error": str(e), "output": e.output}
    

# Ruta a la carpeta de imágenes
img_dir = Path("D:/Taller de investigacion/scraping/CuscoTrends/scraping/Analisis_Data/img")
app.mount("/img", StaticFiles(directory=img_dir), name="img")

@app.get("/listar-imagenes/{tipo}")
async def listar_imagenes(tipo: str, request: Request):
    """
    Endpoint para listar imágenes disponibles en el directorio especificado.
    tipo: 'eda' o 'machine_learning'
    """
    dir_path = img_dir / tipo
    if not dir_path.exists() or not dir_path.is_dir():
        return {"message": "Tipo de análisis no encontrado."}

    # Construir URL completa de la imagen
    imagenes = [
        {
            "nombre": file,
            "url": f"{request.base_url}img/{tipo}/{file}"
        }
        for file in os.listdir(dir_path) if file.endswith(".png")
    ]

    return {"imagenes": imagenes}