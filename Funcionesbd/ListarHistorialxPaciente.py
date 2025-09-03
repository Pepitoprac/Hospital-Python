import sqlite3


def listar_historial_pacientes():
    conexion = sqlite3.connect("hospital.db")
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT p.id, p.nombre, COUNT(hc.id) as consultas
        FROM paciente p
        LEFT JOIN historia_clinica hc ON p.id = hc.paciente_id
        GROUP BY p.id, p.nombre
    """)
    resumen = cursor.fetchall()
    conexion.close()
    return resumen