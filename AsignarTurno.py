import sqlite3


def asignarturno(paciente_id, medico_id, fecha, hora, urgencia, area_id):
    conexion = sqlite3.connect("hospital.db")
    cursor = conexion.cursor()
    try:
        cursor.execute("""
            INSERT INTO turno (paciente_id, medico_id, fecha, hora, urgencia, area_id)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (paciente_id, medico_id, fecha, hora, urgencia, area_id))
        conexion.commit()
        return {"ok": True, "msg": "Turno asignado correctamente"}
    except sqlite3.IntegrityError as e:
        return {"ok": False, "msg": f"Error: {e}"}
    finally:
        conexion.close()