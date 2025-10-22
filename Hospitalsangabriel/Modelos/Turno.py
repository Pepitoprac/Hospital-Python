from Modelos.Paciente import Paciente
from Modelos.Medico import Medico
from Modelos.Area import Area
import sqlite3

class Turno:
    def __init__(self, paciente: Paciente, medico: Medico, fecha: str, hora: str, urgencia: int, area: Area):
        self.paciente = paciente
        self.medico = medico
        self.fecha = fecha
        self.hora = hora
        self.urgencia = urgencia  # 1 a 4
        self.area = area

    @staticmethod
    def crearTabla():
        conexion = sqlite3.connect("hospital.db")
        cursor = conexion.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS turno (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                paciente_id INTEGER NOT NULL,
                medico_id INTEGER NOT NULL,
                fecha TEXT NOT NULL,
                hora TEXT NOT NULL,
                urgencia INTEGER NOT NULL CHECK(urgencia BETWEEN 1 AND 4),
                area_id INTEGER NOT NULL,
                FOREIGN KEY(paciente_id) REFERENCES paciente(id),
                FOREIGN KEY(medico_id) REFERENCES medico(id),
                FOREIGN KEY(area_id) REFERENCES area(id)
            );
        """)
        
        conexion.commit()
        conexion.close()
