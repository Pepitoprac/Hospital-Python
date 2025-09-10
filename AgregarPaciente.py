import sqlite3

def agregar_paciente():
    dni = input("DNI del paciente: ").strip()
    nombre = input("Nombre del paciente: ").strip()
    fecha = input("Fecha de nacimiento (YYYY-MM-DD): ").strip()

    # Validación básica
    if not dni or not nombre or not fecha:
        print("❌ Error: Todos los campos son obligatorios.")
        return

    # Conexión a la base de datos
    conexion = sqlite3.connect("hospital.db")
    cursor = conexion.cursor()

    try:
        cursor.execute("""
            INSERT INTO paciente (dni, nombre, fechaNacimiento)
            VALUES (?, ?, ?)
        """, (dni, nombre, fecha))
        conexion.commit()
        print("✅ Paciente agregado correctamente.")
    except sqlite3.IntegrityError:
        print("❌ Error: El DNI ya existe.")
    finally:
        conexion.close()
