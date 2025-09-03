from Modelos.Area import Area

class Especialidad:
    def __init__(self, id_especialidad, area: Area, nombre):
        self.id_especialidad = id_especialidad
        self.area = area  # objeto Area
        self.nombre = nombre

    @staticmethod
    def crearTabla():
        import sqlite3
        conexion = sqlite3.connect("hospital.db")
        cursor = conexion.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS especialidad (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                area_id INTEGER NOT NULL,
                nombre TEXT NOT NULL,
                FOREIGN KEY(area_id) REFERENCES area(id)
            );
        """)
        
        conexion.commit()
        conexion.close()
