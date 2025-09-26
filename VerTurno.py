import sqlite3
import tkinter as tk
from tkinter import ttk

DB = "hospital.db"
"""Lo usamos como historial de turnos"""
def conectar_db():
    return sqlite3.connect(DB)


def ver_turnos():
    conexion = conectar_db()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT t.id, m.nombre AS medico, t.fecha, t.hora, t.urgencia
            FROM turno t
            JOIN medico m ON t.medico_id = m.id
            WHERE t.paciente_id = ?
              AND date(t.fecha) < date('now')   -- turnos pasados
            ORDER BY t.fecha DESC, t.hora DESC
    """)
    turnos = cursor.fetchall()
    conexion.close()
    return turnos

def ventana_turnos(parent):
    # --- Nueva ventana ---
    win = tk.Toplevel(parent)
    win.title("Listado de Turnos")
    win.geometry("700x400")

    # Tabla
    columnas = ("ID", "Paciente", "Médico", "Fecha", "Hora", "Urgencia")
    tabla_turnos = ttk.Treeview(win, columns=columnas, show="headings", height=15)

    for col in columnas:
        tabla_turnos.heading(col, text=col)
        tabla_turnos.column(col, width=100)

    tabla_turnos.pack(fill="both", expand=True, padx=10, pady=10)

    def mostrar_turnos():
        # Limpiar tabla antes de cargar
        for row in tabla_turnos.get_children():
            tabla_turnos.delete(row)

        # Cargar datos
        for turno in ver_turnos():
            tabla_turnos.insert("", "end", values=turno)

    # Botón para refrescar turnos
    btn_cargar = tk.Button(win, text="Actualizar lista de turnos", command=mostrar_turnos)
    btn_cargar.pack(pady=5)

    # Mostrar automáticamente al abrir
    mostrar_turnos()