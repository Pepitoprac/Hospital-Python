import sqlite3


def verturnopormedico(medico_id):
    conexion = sqlite3.connect("hospital.db")
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT t.id, p.nombre, t.fecha, t.hora, t.urgencia
        FROM turno t
        JOIN paciente p ON t.paciente_id = p.id
        WHERE t.medico_id = ?
        ORDER BY t.urgencia DESC, t.fecha, t.hora
    """, (medico_id,))
    turnos = cursor.fetchall()
    conexion.close()
    return turnos