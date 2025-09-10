from Area import Area
from Especialidad import Especialidad
from Medico import Medico
from Paciente import Paciente
from Turno import Turno
from HistoriaClinica import HistoriaClinica
from autenticador import Auth


def inicializar_bd():
    Auth.crearTabla()
    Area.crearTabla()
    Especialidad.crearTabla()
    Medico.crearTabla()
    Paciente.crearTabla()
    Turno.crearTabla()
    HistoriaClinica.crearTabla()    
    print("Tablas creadas y base de datos inicializada.")

if __name__ == "__main__":
    inicializar_bd()