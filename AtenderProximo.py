import tkinter as tk
from tkinter import messagebox
import sqlite3

# -------------------------
# Función atender próximo
# -------------------------
def atenderproximo(medico_id):
    conexion = sqlite3.connect("hospital.db")
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT t.id, t.paciente_id, p.dni, p.nombre, 
               t.matriculamedico, t.dnipaciente, 
               t.area_id, a.descripcion, 
               t.fecha, t.hora, t.urgencia
        FROM turno t
        JOIN paciente p ON t.paciente_id = p.id
        JOIN area a ON t.area_id = a.id
        WHERE t.medico_id = ?
        ORDER BY t.urgencia DESC, t.fecha, t.hora
        LIMIT 1
    """, (medico_id,))
    turno = cursor.fetchone()

    if not turno:
        conexion.close()
        return {"ok": False, "msg": "No hay turnos pendientes"}

    (turno_id, paciente_id, dni_paciente, nombre_paciente, 
     matricula_medico, dni_turno, 
     area_id, area_desc, fecha, hora, urgencia) = turno

    # Guardar en historia clínica
    cursor.execute("""
        INSERT INTO historia_clinica (paciente_id, medico_id, area_id, fecha, hora, detalles_sintomas)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (paciente_id, medico_id, area_id, fecha, hora, "Consulta realizada"))

    # Eliminar turno
    cursor.execute("DELETE FROM turno WHERE id = ?", (turno_id,))
    conexion.commit()
    conexion.close()

    return {
        "ok": True,
        "msg": f"Turno {turno_id} atendido y registrado en historia clínica",
        "paciente": {"dni": dni_paciente, "nombre": nombre_paciente},
        "medico": matricula_medico,
        "area": area_desc,
        "fecha": fecha,
        "hora": hora,
        "urgencia": urgencia
    }


# -------------------------
# Interfaz Tkinter
# -------------------------
def ventana_atenderproximo():
    ventana = tk.Toplevel()
    ventana.title("Atender Próximo Turno")

    # Label y campo de entrada
    tk.Label(ventana, text="ID Médico").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    entry_medico = tk.Entry(ventana)
    entry_medico.grid(row=0, column=1, padx=10, pady=5)

    # Función que se ejecuta al presionar botón
    def procesar():
        medico_id = entry_medico.get().strip()

        if not medico_id:
            messagebox.showwarning("Error", "Debe ingresar el ID del médico")
            return

        resultado = atenderproximo(medico_id)
        if resultado["ok"]:
            resumen = (
                f"✅ Turno atendido correctamente\n\n"
                f"Paciente: {resultado['paciente']['dni']} - {resultado['paciente']['nombre']}\n"
                f"Médico (Matrícula): {resultado['medico']}\n"
                f"Área: {resultado['area']}\n"
                f"Fecha: {resultado['fecha']}  Hora: {resultado['hora']}\n"
                f"Urgencia: {resultado['urgencia']}"
            )
            messagebox.showinfo("Éxito", resumen)
            entry_medico.delete(0, tk.END)
        else:
            messagebox.showwarning("Aviso", resultado["msg"])

    # Botón para atender
    tk.Button(
        ventana, 
        text="Atender Próximo", 
        command=procesar, 
        bg="lightblue"
    ).grid(row=1, column=0, columnspan=2, pady=10)
