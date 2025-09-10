import sqlite3
def listarpaciente():
    conexion = sqlite3.connect("hospital.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT id, dni, nombre, fechaNacimiento FROM paciente")
    pacientes = cursor.fetchall()
    conexion.close()
    return pacientes