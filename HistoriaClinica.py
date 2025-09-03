import sqlite3
from Paciente import Paciente
from Medico import Medico
from Area import Area

class HistoriaClinica:
    def __init__(self, id_historia, paciente: Paciente, medico: Medico, area: Area, fecha, hora, detalles_sintomas):
        self.id_historia = id_historia
        self.paciente = paciente
        self.medico = medico
        self.area = area
        self.fecha = fecha
        self.hora = hora
        self.detalles_sintomas = detalles_sintomas

    @staticmethod
    def crearTabla():
        conexion = sqlite3.connect("hospital.db")
        cursor = conexion.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS historia_clinica (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                paciente_id INTEGER NOT NULL,
                medico_id INTEGER NOT NULL,
                area_id INTEGER NOT NULL,
                fecha TEXT NOT NULL,
                hora TEXT NOT NULL,
                detalles_sintomas TEXT,
                FOREIGN KEY(paciente_id) REFERENCES paciente(id),
                FOREIGN KEY(medico_id) REFERENCES medico(id),
                FOREIGN KEY(area_id) REFERENCES area(id)
            );
        """)
        
        conexion.commit()
        conexion.close()
