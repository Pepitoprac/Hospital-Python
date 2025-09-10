from Especialidad import Especialidad
import sqlite3

class Medico:
    def __init__(self, id_medico, nombre, matricula, especialidad: Especialidad):
        self.id_medico = id_medico
        self.nombre = nombre
        self.matricula = matricula
        self.especialidad = especialidad
        
    @staticmethod
    def crearTabla():
        conexion = sqlite3.connect("hospital.db")
        cursor = conexion.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS medico (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                matricula TEXT NOT NULL,
                especialidad_id INTEGER,
                FOREIGN KEY(especialidad_id) REFERENCES especialidad(id)
            );
        """)
        
        conexion.commit()
        conexion.close()