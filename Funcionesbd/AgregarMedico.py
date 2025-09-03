import sqlite3
from Modelos import Medico
# --------------------
# Funciones de médicos
# --------------------
def agregarmedico(nombre, matricula, especialidad_id):
    conexion = sqlite3.connect("hospital.db")
    cursor = conexion.cursor()
    try:
        cursor.execute("""
            INSERT INTO medico (nombre, matricula, especialidad_id)
            VALUES (?, ?, ?)
        """, (nombre, matricula, especialidad_id))
        conexion.commit()
        return {"ok": True, "msg": "Médico agregado correctamente"}
    except sqlite3.IntegrityError as e:
        return {"ok": False, "msg": f"Error: {e}"}
    finally:
        conexion.close()