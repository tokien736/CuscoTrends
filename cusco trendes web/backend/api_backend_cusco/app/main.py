from fastapi import FastAPI, HTTPException
from app.database import get_db_connection
from app.models import obtener_usuarios, crear_usuario, obtener_usuario_por_id, actualizar_usuario, eliminar_usuario
from app.schemas import UsuarioCreate, UsuarioResponse

app = FastAPI()

@app.get("/usuarios/", response_model=list[UsuarioResponse])
def listar_usuarios():
    connection = get_db_connection()
    if connection:
        usuarios = obtener_usuarios(connection)
        connection.close()
        if usuarios:
            return usuarios
        raise HTTPException(status_code=404, detail="No se encontraron usuarios")
    raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos")

@app.post("/usuarios/", response_model=UsuarioResponse)
def crear_usuario_api(usuario: UsuarioCreate):
    connection = get_db_connection()
    if connection:
        usuario_id = crear_usuario(connection, usuario.username, "", usuario.password)
        connection.close()
        if usuario_id:
            return {"id": usuario_id, "username": usuario.username}
        raise HTTPException(status_code=400, detail="No se pudo crear el usuario")
    raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos")

@app.get("/usuarios/{usuario_id}", response_model=UsuarioResponse)
def obtener_usuario_api(usuario_id: int):
    connection = get_db_connection()
    if connection:
        usuario = obtener_usuario_por_id(connection, usuario_id)
        connection.close()
        if usuario:
            return usuario
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos")

@app.put("/usuarios/{usuario_id}")
def actualizar_usuario_api(usuario_id: int, usuario: UsuarioCreate):
    connection = get_db_connection()
    if connection:
        actualizar_usuario(connection, usuario_id, usuario.username, "")
        connection.close()
        return {"message": "Usuario actualizado correctamente"}
    raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos")

@app.delete("/usuarios/{usuario_id}")
def eliminar_usuario_api(usuario_id: int):
    connection = get_db_connection()
    if connection:
        eliminar_usuario(connection, usuario_id)
        connection.close()
        return {"message": "Usuario eliminado correctamente"}
    raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos")
