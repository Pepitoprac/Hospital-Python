from Area import Area
from Especialidad import Especialidad
from Medico import Medico
from Paciente import Paciente
from Turno import Turno
from HistoriaClinica import HistoriaClinica


def inicializar_bd():
    Area.crearTabla()
    Especialidad.crearTabla()
    Paciente.crearTabla()
    Medico.crearTabla()
    Turno.crearTabla()
    HistoriaClinica.crearTabla()
    print("Tablas creadas y base de datos inicializada.")

if __name__ == "__main__":
    inicializar_bd()