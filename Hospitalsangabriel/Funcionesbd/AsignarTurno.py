import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from tkcalendar import DateEntry
from rutadb import DB as RutaDb

DB_PATH = RutaDb

def asignarturno():
    ventana = tk.Toplevel()
    ventana.title("Asignar Turno [Panel Admin]")

    # -----------------------------
    # Paciente (DNI en combobox)
    # -----------------------------
    tk.Label(ventana, text="Paciente (DNI - Nombre)").grid(row=0, column=0, padx=10, pady=5, sticky="w")

    combo_paciente = ttk.Combobox(ventana, state="readonly", width=40)
    combo_paciente.grid(row=0, column=1, padx=10, pady=5)

    with sqlite3.connect(DB_PATH) as conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT id, dni, nombre FROM paciente")
        pacientes = cursor.fetchall()

    # Mapear correctamente (sin p[3])
    paciente_map = {f"{p[1]} - {p[2]}": (p[0], p[1], p[2]) for p in pacientes}
    combo_paciente["values"] = list(paciente_map.keys())

    # -----------------------------
    # Médico (combobox matrícula - nombre)
    # -----------------------------
    tk.Label(ventana, text="Médico (Matrícula - Nombre)").grid(row=2, column=0, padx=10, pady=5, sticky="w")

    combo_medico = ttk.Combobox(ventana, state="readonly", width=40)
    combo_medico.grid(row=2, column=1, padx=10, pady=5)

    with sqlite3.connect(DB_PATH) as conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT id, matricula, nombre, especialidad_id FROM medico")
        medicos = cursor.fetchall()

    medico_map = {f"{m[1]} - {m[2]}": (m[0], m[1], m[3]) for m in medicos}
    combo_medico["values"] = list(medico_map.keys())

    # -----------------------------
    # Área (automática según médico)
    # -----------------------------
    tk.Label(ventana, text="Área").grid(row=3, column=0, padx=10, pady=5, sticky="w")

    entry_area = tk.Entry(ventana, state="readonly", width=40)
    entry_area.grid(row=3, column=1, padx=10, pady=5)

    def actualizar_area(event):
        seleccionado = combo_medico.get()
        if not seleccionado:
            return
        _, _, especialidad_id = medico_map[seleccionado]
        with sqlite3.connect(DB_PATH) as conexion:
            cursor = conexion.cursor()
            cursor.execute("""
                SELECT a.id, a.descripcion
                FROM especialidad e
                JOIN area a ON e.area_id = a.id
                WHERE e.id = ?
            """, (especialidad_id,))
            row = cursor.fetchone()
        if row:
            area_id, descripcion = row
            entry_area.config(state="normal")
            entry_area.delete(0, tk.END)
            entry_area.insert(0, descripcion)
            entry_area.config(state="readonly")
            entry_area.area_id = area_id  # guardamos el ID

    combo_medico.bind("<<ComboboxSelected>>", actualizar_area)

    # -----------------------------
    # Fecha y Hora
    # -----------------------------
    tk.Label(ventana, text="Fecha (YYYY-MM-DD)").grid(row=4, column=0, padx=10, pady=5, sticky="w")
    entry_fecha = DateEntry(ventana, date_pattern="yyyy-mm-dd")
    entry_fecha.grid(row=4, column=1, padx=10, pady=5)

    tk.Label(ventana, text="Hora (HH:MM)").grid(row=5, column=0, padx=10, pady=5, sticky="w")
    entry_hora = tk.Entry(ventana)
    entry_hora.grid(row=5, column=1, padx=10, pady=5)

    # -----------------------------
    # Urgencia (opcional)
    # -----------------------------
    tk.Label(ventana, text="Urgencia (0 = Normal / 1 = Urgente)").grid(row=6, column=0, padx=10, pady=5, sticky="w")
    entry_urgencia = tk.Entry(ventana)
    entry_urgencia.grid(row=6, column=1, padx=10, pady=5)

    # -----------------------------
    # Guardar turno
    # -----------------------------
    def guardar():
        paciente_sel = combo_paciente.get().strip()
        medico_sel = combo_medico.get().strip()
        fecha = entry_fecha.get().strip()
        hora = entry_hora.get().strip()
        area_id = getattr(entry_area, "area_id", None)
        urgencia = entry_urgencia.get().strip() or "0"

        if not paciente_sel or not medico_sel or not fecha or not hora or not area_id:
            messagebox.showwarning("Error", "Todos los campos son obligatorios")
            return

        paciente_id, dni_paciente, _ = paciente_map[paciente_sel]
        medico_id, matricula, _ = medico_map[medico_sel]

        with sqlite3.connect(DB_PATH) as conexion:
            cursor = conexion.cursor()
            cursor.execute("""
                INSERT INTO turno (paciente_id, medico_id, fecha, hora, area_id, urgencia)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (paciente_id, medico_id, fecha, hora, area_id, urgencia))
            conexion.commit()

        messagebox.showinfo("Éxito", "Turno asignado correctamente")

        # Limpiar campos
        combo_paciente.set("")
        combo_medico.set("")
        entry_area.config(state="normal")
        entry_area.delete(0, tk.END)
        entry_area.config(state="readonly")
        entry_fecha.delete(0, tk.END)
        entry_hora.delete(0, tk.END)
        entry_urgencia.delete(0, tk.END)

    # -----------------------------
    # Botón Confirmar Turno
    # -----------------------------
    tk.Button(ventana, text="Confirmar Turno", command=guardar, bg="lightgreen").grid(
        row=7, column=0, columnspan=2, pady=10
    )
