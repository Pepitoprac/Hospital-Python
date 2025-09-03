import sqlite3

class Area:
    def __init__(self, id_area, descripcion):
        self.id_area = id_area
        self.descripcion = descripcion

    @staticmethod
    def crearTabla():
        conexion = sqlite3.connect("hospital.db")
        cursor = conexion.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS area (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                descripcion TEXT
            );
        """)
        
        conexion.commit()
        conexion.close()
