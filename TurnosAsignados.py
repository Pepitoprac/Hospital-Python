import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

DB_PATH = "hospital.db"

# --------------------
# Ver turnos por médico (solo hoy)
# --------------------
def verturnopormedico2(medico_id):
    with sqlite3.connect(DB_PATH) as conexion:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT t.id, p.nombre, t.fecha, t.hora, t.urgencia
            FROM turno t
            JOIN paciente p ON t.paciente_id = p.id
            WHERE t.medico_id = ?
            AND t.fecha = date('now')  
            ORDER BY t.urgencia DESC, t.hora
        """, (medico_id,))
        return cursor.fetchall()

# --------------------
# Ventana Tkinter - Turnos del médico logueado
# --------------------
def ventana_turnos_asignados(medico_id):
    ventana = tk.Toplevel()
    ventana.title("Mis Turnos Asignados")
    ventana.geometry("800x450")

    tk.Label(ventana, text="Turnos asignados para hoy", font=("Arial", 12, "bold")).pack(pady=5)

    # Tabla de turnos
    columnas = ("ID Turno", "Paciente", "Fecha", "Hora", "Urgencia")
    tabla = ttk.Treeview(ventana, columns=columnas, show="headings", height=15)
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, anchor="center", width=150)
    tabla.pack(fill="both", expand=True, padx=10, pady=10)

    # Función para cargar turnos
    def cargar_turnos():
        for row in tabla.get_children():
            tabla.delete(row)

        turnos = verturnopormedico2(medico_id)

        if turnos:
            for turno in turnos:
                tabla.insert("", tk.END, values=turno)
        else:
            messagebox.showinfo("Sin turnos", "No tenés turnos asignados para hoy")

    # Botón actualizar
    tk.Button(ventana, text="Actualizar", command=cargar_turnos, bg="lightgreen").pack(pady=5)

    # Cargar automáticamente al abrir
    cargar_turnos()
