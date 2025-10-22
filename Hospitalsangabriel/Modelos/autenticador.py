# auth.py
import sqlite3

class Auth:
    def __init__(self, id_usuario, nombre, contrasena, rol):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.contrasena = contrasena
        self.rol = rol

    @staticmethod
    def crearTabla():
        conexion = sqlite3.connect("hospital.db")
        cursor = conexion.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuario (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT,
                contrasena TEXT,
                rol TEXT
            );
        """)
        conexion.commit()
        conexion.close()