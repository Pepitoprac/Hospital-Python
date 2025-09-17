import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

def asignarturno():
    ventana = tk.Toplevel()
    ventana.title("Asignar Turno [Panel Admin]")

    # -----------------------------
    # Paciente (DNI en combobox)
    # -----------------------------
    tk.Label(ventana, text="Paciente (DNI - Nombre)").grid(row=0, column=0, padx=10, pady=5, sticky="w")

    combo_paciente = ttk.Combobox(ventana, state="readonly")
    combo_paciente.grid(row=0, column=1, padx=10, pady=5)

    # Cargar pacientes desde la BD
    conexion = sqlite3.connect("hospital.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT id, dni, nombre FROM paciente")
    pacientes = cursor.fetchall()
    conexion.close()

    paciente_map = {f"{p[1]} - {p[2]}": (p[0], p[1]) for p in pacientes}  # (id, dni)
    combo_paciente["values"] = list(paciente_map.keys())

    # -----------------------------
    # Médico (matrícula)
    # -----------------------------
    tk.Label(ventana, text="Matrícula Médico").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    entry_matricula = tk.Entry(ventana)
    entry_matricula.grid(row=1, column=1, padx=10, pady=5)

    # -----------------------------
    # Fecha y Hora
    # -----------------------------
    tk.Label(ventana, text="Fecha (YYYY-MM-DD)").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    entry_fecha = tk.Entry(ventana)
    entry_fecha.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(ventana, text="Hora (HH:MM)").grid(row=3, column=0, padx=10, pady=5, sticky="w")
    entry_hora = tk.Entry(ventana)
    entry_hora.grid(row=3, column=1, padx=10, pady=5)

    # -----------------------------
    # Urgencia
    # -----------------------------
    tk.Label(ventana, text="Urgencia (0/1)").grid(row=4, column=0, padx=10, pady=5, sticky="w")
    entry_urgencia = tk.Entry(ventana)
    entry_urgencia.grid(row=4, column=1, padx=10, pady=5)

    # -----------------------------
    # Área (combobox)
    # -----------------------------
    tk.Label(ventana, text="Área").grid(row=5, column=0, padx=10, pady=5, sticky="w")

    combo_area = ttk.Combobox(ventana, state="readonly")
    combo_area.grid(row=5, column=1, padx=10, pady=5)

    conexion = sqlite3.connect("hospital.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT id, descripcion FROM area")
    areas = cursor.fetchall()
    conexion.close()

    area_map = {f"{a[0]} - {a[1]}": a[0] for a in areas}
    combo_area["values"] = list(area_map.keys())

    # -----------------------------
    # Guardar turno
    # -----------------------------
    def guardar():
        paciente_sel = combo_paciente.get().strip()
        matricula = entry_matricula.get().strip()
        fecha = entry_fecha.get().strip()
        hora = entry_hora.get().strip()
        urgencia = entry_urgencia.get().strip()
        area_sel = combo_area.get().strip()

        if not paciente_sel or not matricula or not fecha or not hora or not urgencia or not area_sel:
            messagebox.showwarning("Error", "Todos los campos son obligatorios")
            return

        conexion = sqlite3.connect("hospital.db")
        cursor = conexion.cursor()

        try:
            # Datos del paciente
            paciente_id, dni_paciente = paciente_map[paciente_sel]

            # Buscar médico por matrícula
            cursor.execute("SELECT id FROM medico WHERE matricula = ?", (matricula,))
            medico_row = cursor.fetchone()

            if not medico_row:
                messagebox.showerror("Error", f"No existe un médico con matrícula {matricula}")
                return

            medico_id = medico_row[0]
            area_id = area_map[area_sel]

            # Insertar turno con todo
            cursor.execute("""
                INSERT INTO turno (paciente_id, medico_id, fecha, hora, urgencia, area_id, matriculamedico, dnipaciente)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (paciente_id, medico_id, fecha, hora, urgencia, area_id, matricula, dni_paciente))
            conexion.commit()

            messagebox.showinfo("Éxito", "Turno asignado correctamente")

            # Limpiar campos
            combo_paciente.set("")
            entry_matricula.delete(0, tk.END)
            entry_fecha.delete(0, tk.END)
            entry_hora.delete(0, tk.END)
            entry_urgencia.delete(0, tk.END)
            combo_area.set("")

        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Error al asignar el turno. Verifique los datos.")
        finally:
            conexion.close()

    # -----------------------------
    # Botón Confirmar Turno
    # -----------------------------
    tk.Button(ventana, text="Confirmar Turno", command=guardar, bg="lightgreen").grid(
        row=6, column=0, columnspan=2, pady=10
    )
