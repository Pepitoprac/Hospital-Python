import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
from rutadb import DB as RutaDb

DB_PATH = RutaDb

def obtener_turnos(medico_id=None, solo_pendientes=False):
    with sqlite3.connect(DB_PATH) as conexion:
        cursor = conexion.cursor()
        query = """
            SELECT 
                t.id,
                p.nombre AS paciente,
                m.nombre AS medico,
                t.fecha,
                t.hora,
                t.urgencia
            FROM turno t
            JOIN paciente p ON t.paciente_id = p.id
            JOIN medico m ON t.medico_id = m.id
        """
        params = []
        if medico_id is not None:
            query += " WHERE t.medico_id = ?"
            params.append(medico_id)

        query += " ORDER BY t.fecha DESC, t.hora ASC, t.urgencia DESC"
        cursor.execute(query, params)
        turnos = cursor.fetchall()

        if solo_pendientes:
            hoy = datetime.today().strftime("%Y-%m-%d")
            turnos = [t for t in turnos if t[3] >= hoy]

        return turnos

def ventana_turnos_medico_logueado():
    ventana = tk.Toplevel()
    ventana.title("Turnos Médicos")
    ventana.geometry("950x500")

    tk.Label(ventana, text="Seleccione médico:").pack(pady=5)
    medicos_combo = ttk.Combobox(ventana, state="readonly")
    medicos_combo.pack(pady=5)

    with sqlite3.connect(DB_PATH) as conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT id, nombre FROM medico")
        medicos = cursor.fetchall()
        if not medicos:
            messagebox.showwarning("Atención", "No hay médicos cargados.")
            ventana.destroy()
            return
        medicos_map = {f"{m[1]} (ID:{m[0]})": m[0] for m in medicos}
        medicos_combo["values"] = list(medicos_map.keys())
        medicos_combo.set(list(medicos_map.keys())[0])

    solo_pendientes_var = tk.BooleanVar(value=True)
    tk.Checkbutton(
        ventana,
        text="Mostrar solo turnos pendientes",
        variable=solo_pendientes_var,
        command=lambda: cargar_turnos()
    ).pack(pady=5)

    columnas = ("ID Turno", "Paciente", "Médico", "Fecha", "Hora", "Urgencia")
    tabla = ttk.Treeview(ventana, columns=columnas, show="headings", height=15)
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, anchor="center", width=140)
    tabla.pack(fill="both", expand=True, padx=10, pady=10)

    urgencia_map = {0: "Normal", 1: "Leve", 2: "Moderada", 3: "Grave", 4: "Crítica"}

    def cargar_turnos():
        for row in tabla.get_children():
            tabla.delete(row)
        medico_sel = medicos_combo.get()
        medico_id = medicos_map.get(medico_sel)
        turnos = obtener_turnos(medico_id=medico_id, solo_pendientes=solo_pendientes_var.get())
        if turnos:
            for t in turnos:
                turno_id, paciente, medico, fecha, hora, urgencia = t
                tabla.insert("", tk.END, values=(turno_id, paciente, medico, fecha, hora, urgencia_map.get(urgencia, "—")))
        else:
            tabla.insert("", tk.END, values=("—", "—", "—", "—", "—", "—"))

    medicos_combo.bind("<<ComboboxSelected>>", lambda e: cargar_turnos())
    tk.Button(ventana, text="Actualizar lista", command=cargar_turnos, bg="lightgreen").pack(pady=5)
    cargar_turnos()
