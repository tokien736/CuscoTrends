from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# Configuración base para SQLAlchemy
Base = declarative_base()

# Definición del modelo UsuarioDB
class UsuarioDB(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

# Funciones CRUD para la tabla de usuarios (si no usas ORM, puedes usar raw SQL)
def obtener_usuarios(connection):
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios")
        return cursor.fetchall()
    except Exception as e:
        print(f"Error al obtener usuarios: {e}")
        return None

def crear_usuario(connection, nombre, email, password):
    try:
        cursor = connection.cursor()
        query = "INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)"
        cursor.execute(query, (nombre, email, password))
        connection.commit()
        return cursor.lastrowid
    except Exception as e:
        print(f"Error al crear usuario: {e}")
        return None

def obtener_usuario_por_id(connection, usuario_id):
    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM usuarios WHERE id = %s"
        cursor.execute(query, (usuario_id,))
        return cursor.fetchone()
    except Exception as e:
        print(f"Error al obtener usuario: {e}")
        return None

def actualizar_usuario(connection, usuario_id, nombre, email):
    try:
        cursor = connection.cursor()
        query = "UPDATE usuarios SET nombre = %s, email = %s WHERE id = %s"
        cursor.execute(query, (nombre, email, usuario_id))
        connection.commit()
    except Exception as e:
        print(f"Error al actualizar usuario: {e}")

def eliminar_usuario(connection, usuario_id):
    try:
        cursor = connection.cursor()
        query = "DELETE FROM usuarios WHERE id = %s"
        cursor.execute(query, (usuario_id,))
        connection.commit()
    except Exception as e:
        print(f"Error al eliminar usuario: {e}")
