import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

DB_PATH = "hospital.db"

# --------------------
# Ver turnos del médico logueado
# --------------------
def verturnos_medico_logueado(medico_id):
    with sqlite3.connect(DB_PATH) as conexion:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT 
                t.id,
                p.nombre AS paciente,
                t.fecha,
                t.hora,
                p.urgencia
            FROM turno t
            JOIN paciente p ON t.paciente_id = p.id
            WHERE t.medico_id = ?
            ORDER BY t.fecha DESC, t.hora ASC, p.urgencia DESC
        """, (medico_id,))
        return cursor.fetchall()

# --------------------
# Ventana Tkinter - Turnos del médico logueado
# --------------------
def ventana_turnos_medico_logueado(medico_id, nombre_medico=None):
    ventana = tk.Toplevel()
    ventana.title("Turnos del Médico Logueado")
    ventana.geometry("800x450")

    titulo = f"Turnos asignados a {nombre_medico}" if nombre_medico else "Turnos asignados"
    tk.Label(ventana, text=titulo, font=("Arial", 12, "bold")).pack(pady=5)

    # Tabla de turnos
    columnas = ("ID Turno", "Paciente", "Fecha", "Hora", "Urgencia")
    tabla = ttk.Treeview(ventana, columns=columnas, show="headings", height=15)
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, anchor="center", width=150)
    tabla.pack(fill="both", expand=True, padx=10, pady=10)

    # Mapeo de niveles de urgencia
    urgencia_map = {
        1: "Leve",
        2: "Moderada",
        3: "Grave",
        4: "Crítica"
    }

    # Función para cargar turnos
    def cargar_turnos():
        for row in tabla.get_children():
            tabla.delete(row)

        turnos = verturnos_medico_logueado(medico_id)

        if turnos:
            for turno in turnos:
                turno_id, paciente, fecha, hora, urgencia = turno
                urgencia_txt = urgencia_map.get(urgencia, "—")
                tabla.insert("", tk.END, values=(turno_id, paciente, fecha, hora, urgencia_txt))
        else:
            messagebox.showinfo("Sin turnos", "No tenés turnos asignados.")

    # Botón actualizar
    tk.Button(ventana, text="Actualizar lista", command=cargar_turnos, bg="lightgreen").pack(pady=5)

    # Cargar automáticamente al abrir
    cargar_turnos()
