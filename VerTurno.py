import sqlite3


def verturno(id_turno):
    conexion = sqlite3.connect("hospital.db")
    cursor = conexion.cursor()

    print(f"Buscando turno con ID: {id_turno}")  # DEBUG
    print("OPAAA")

    cursor.execute("""
        SELECT id, paciente_id, medico_id, fecha, hora, urgencia, area_id
            FROM turno
            WHERE id = ?;
    """, (id_turno,))
    
    turno = cursor.fetchone()
    print(f"Resultado: {turno}")  # DEBUG

    conexion.close()
    return turno
