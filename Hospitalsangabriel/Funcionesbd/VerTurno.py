import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from rutadb import DB as RutaDb

DB_PATH = RutaDb

def conectar_db():
    return sqlite3.connect(DB_PATH)

def obtener_pacientes():
    with conectar_db() as conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT id, dni, nombre FROM paciente ORDER BY nombre")
        return cursor.fetchall()

def ver_turnos(paciente_id):
    with conectar_db() as conexion:
        cursor = conexion.cursor()
        cursor.execute("""
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
            WHERE t.paciente_id = ?
              AND date(t.fecha) < date('now')
            ORDER BY t.fecha DESC, t.hora DESC
        """, (paciente_id,))
        return cursor.fetchall()

def ventana_turnos(parent):
    win = tk.Toplevel(parent)
    win.title("Historial de Turnos (Pasados)")
    win.geometry("750x450")

    tk.Label(win, text="Seleccione un paciente:").pack(pady=5)
    pacientes = obtener_pacientes()

    if not pacientes:
        messagebox.showwarning("Sin datos", "No hay pacientes registrados.")
        win.destroy()
        return

    paciente_map = {f"{p[2]} (DNI {p[1]})": p[0] for p in pacientes}
    combo_paciente = ttk.Combobox(win, values=list(paciente_map.keys()), state="readonly", width=50)
    combo_paciente.pack(pady=5)

    columnas = ("ID", "Paciente", "Médico", "Fecha", "Hora", "Urgencia")
    tabla_turnos = ttk.Treeview(win, columns=columnas, show="headings", height=15)

    for col in columnas:
        tabla_turnos.heading(col, text=col)
        tabla_turnos.column(col, width=120, anchor="center")

    tabla_turnos.pack(fill="both", expand=True, padx=10, pady=10)

    def mostrar_turnos():
        for row in tabla_turnos.get_children():
            tabla_turnos.delete(row)

        seleccionado = combo_paciente.get()
        if not seleccionado:
            messagebox.showwarning("Aviso", "Seleccione un paciente.")
            return

        paciente_id = paciente_map[seleccionado]
        turnos = ver_turnos(paciente_id)

        if not turnos:
            messagebox.showinfo("Sin resultados", "El paciente no tiene turnos pasados.")
            return

        for turno in turnos:
            turno_id, paciente, medico, fecha, hora, urgencia = turno
            urgencia = urgencia if urgencia is not None else "—"
            tabla_turnos.insert("", "end", values=(turno_id, paciente, medico, fecha, hora, urgencia))

    tk.Button(win, text="Ver Turnos Pasados", command=mostrar_turnos, bg="lightblue").pack(pady=5)
