import sqlite3

def listarmedico():
    conexion = sqlite3.connect("hospital.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre, matricula, especialidad_id FROM medico")
    medicos = cursor.fetchall()
    conexion.close()
    return medicos
