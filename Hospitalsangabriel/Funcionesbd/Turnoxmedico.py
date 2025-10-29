import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from rutadb import DB as RutaDb

DB_PATH = RutaDb

def obtener_medicos():
    with sqlite3.connect(DB_PATH) as conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT id, matricula, nombre FROM medico")
        return cursor.fetchall()

def verturnopormedico(medico_id):
    with sqlite3.connect(DB_PATH) as conexion:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT 
                t.id AS turno_id,
                p.nombre AS paciente,
                t.fecha,
                t.hora,
                t.urgencia
            FROM turno t
            JOIN paciente p ON t.paciente_id = p.id
            WHERE t.medico_id = ?
              AND t.fecha = date('now')
            ORDER BY t.urgencia DESC, t.hora
        """, (medico_id,))
        return cursor.fetchall()

def ventana_turnos_por_medico():
    ventana = tk.Toplevel()
    ventana.title("Turnos por Médico (Hoy)")
    ventana.geometry("800x450")

    tk.Label(ventana, text="Seleccione un médico:").pack(pady=5)
    medicos = obtener_medicos()

    if not medicos:
        messagebox.showwarning("Aviso", "No hay médicos registrados en la base de datos")
        ventana.destroy()
        return

    medico_map = {f"{m[1]} - {m[2]}": m[0] for m in medicos}
    combo_medico = ttk.Combobox(ventana, values=list(medico_map.keys()), state="readonly", width=50)
    combo_medico.pack(pady=5)

    columnas = ("ID Turno", "Paciente", "Fecha", "Hora", "Urgencia")
    tabla = ttk.Treeview(ventana, columns=columnas, show="headings", height=15)
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, anchor="center", width=150)
    tabla.pack(fill="both", expand=True, padx=10, pady=10)

    def cargar_turnos():
        for row in tabla.get_children():
            tabla.delete(row)

        seleccionado = combo_medico.get()
        if not seleccionado:
            messagebox.showwarning("Aviso", "Seleccione un médico")
            return

        medico_id = medico_map[seleccionado]
        turnos = verturnopormedico(medico_id)

        if turnos:
            for turno in turnos:
                turno_id, paciente, fecha, hora, urgencia = turno
                urgencia = urgencia if urgencia is not None else "—"
                tabla.insert("", tk.END, values=(turno_id, paciente, fecha, hora, urgencia))
        else:
            messagebox.showinfo("Sin turnos", f"El médico {seleccionado} no tiene turnos para hoy")

    tk.Button(ventana, text="Ver Turnos", command=cargar_turnos, bg="lightblue").pack(pady=5)
    tk.Button(ventana, text="Actualizar", command=cargar_turnos, bg="lightgreen").pack(pady=5)
