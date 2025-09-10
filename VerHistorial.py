import sqlite3


def verhistorial():
    conexion = sqlite3.connect("hospital.db")
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT hc.id, p.nombre, m.nombre, a.descripcion, hc.fecha, hc.hora, hc.detalles_sintomas
        FROM historia_clinica hc
        JOIN paciente p ON hc.paciente_id = p.id
        JOIN medico m ON hc.medico_id = m.id
        JOIN area a ON hc.area_id = a.id
    """)
    historial = cursor.fetchall()
    conexion.close()
    return historial