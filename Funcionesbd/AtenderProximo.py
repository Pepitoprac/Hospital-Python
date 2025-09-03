import sqlite3


def atenderproximo(medico_id):
    conexion = sqlite3.connect("hospital.db")
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT t.id, t.paciente_id, t.area_id, t.fecha, t.hora, t.urgencia
        FROM turno t
        WHERE t.medico_id = ?
        ORDER BY t.urgencia DESC, t.fecha, t.hora
        LIMIT 1
    """, (medico_id,))
    turno = cursor.fetchone()

    if not turno:
        conexion.close()
        return {"ok": False, "msg": "No hay turnos pendientes"}

    turno_id, paciente_id, area_id, fecha, hora, urgencia = turno

    # Guardamos en historia clínica
    cursor.execute("""
        INSERT INTO historia_clinica (paciente_id, medico_id, area_id, fecha, hora, detalles_sintomas)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (paciente_id, medico_id, area_id, fecha, hora, "Consulta realizada"))
    
    # Eliminamos turno
    cursor.execute("DELETE FROM turno WHERE id = ?", (turno_id,))
    conexion.commit()
    conexion.close()

    return {"ok": True, "msg": f"Turno {turno_id} atendido y registrado en historia clínica"}