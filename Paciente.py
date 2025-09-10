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
                dni TEXT NOT NULL UNIQUE,
                nombre TEXT NOT NULL,
                fechaNacimiento TEXT
            );
        """)
        
        conexion.commit()
        conexion.close()



        