import sqlite3


def historialporpaciente(paciente_id):
    conexion = sqlite3.connect("hospital.db")
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT hc.id, hc.fecha, hc.hora, hc.detalles_sintomas, m.nombre, a.descripcion
        FROM historia_clinica hc
        JOIN medico m ON hc.medico_id = m.id
        JOIN area a ON hc.area_id = a.id
        WHERE hc.paciente_id = ?
    """, (paciente_id,))
    historial = cursor.fetchall()
    conexion.close()
    return historial