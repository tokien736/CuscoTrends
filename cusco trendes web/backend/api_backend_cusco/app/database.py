import mysql.connector
from mysql.connector import Error

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # Coloca tu contraseña de MySQL aquí
            database="cuscotrends"
        )
        if connection.is_connected():
            print("Conexión exitosa a la base de datos")
            return connection
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None

def cerrar_conexion(connection):
    if connection.is_connected():
        connection.close()
        print("Conexión cerrada correctamente")
