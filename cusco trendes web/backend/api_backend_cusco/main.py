from fastapi import FastAPI
from routers import users  # Importa el enrutador de usuarios

app = FastAPI()

# Incluye el enrutador de usuarios en la app principal
app.include_router(users.router)

@app.get("/")
def read_root():
    return {"message": "¡Bienvenido a FastAPI!"}
