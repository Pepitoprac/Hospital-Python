import sqlite3

class Paciente:
    def __init__(self, idpaciente, dni, nombre, fechaNacimiento):
        self.idpaciente = idpaciente
        self.dni = dni
        self.nombre = nombre
        self.fechaNacimiento = fechaNacimiento

    @staticmethod
    def crearTabla():
        conexion = sqlite3.connect("hospital.db")
        cursor = conexion.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS paciente (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dni TEXT NOT NULL CHECK (length(dni) <= 8) UNIQUE,
                nombre TEXT NOT NULL,
                fechaNacimiento TEXT NOT NULL,
                urgencia INTEGER CHECK (urgencia BETWEEN 1 AND 4)
            );
        """)
        
        conexion.commit()
        conexion.close()



        