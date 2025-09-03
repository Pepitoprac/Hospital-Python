from Modelos.Area import Area
from Modelos.Especialidad import Especialidad
from Modelos.Medico import Medico
from Modelos.Paciente import Paciente
from Modelos.Turno import Turno
from Modelos.HistoriaClinica import HistoriaClinica
from Authenticador.autenticador import Auth


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