import sqlite3


def verturno(id_turno):
    conexion = sqlite3.connect("hospital.db")
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT t.id, p.nombre, m.nombre, t.fecha, t.hora, t.urgencia, a.descripcion
        FROM turno t
        JOIN paciente p ON t.paciente_id = p.id
        JOIN medico m ON t.medico_id = m.id
        JOIN area a ON t.area_id = a.id
        WHERE t.id = ?
    """, (id_turno,))
    turno = cursor.fetchone()
    conexion.close()
    return turno