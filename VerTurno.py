import sqlite3
import tkinter as tk
from tkinter import ttk

DB = "hospital.db"

def conectar_db():
    return sqlite3.connect(DB)

def ver_turnos():
    conexion = conectar_db()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT 
            t.id,
            p.nombre,
            m.nombre,
            t.fecha,
            t.hora,
            t.urgencia
        FROM turno t
        JOIN paciente p ON t.paciente_id = p.id
        JOIN medico m ON t.medico_id = m.id
        ORDER BY t.fecha, t.hora;
    """)
    turnos = cursor.fetchall()
    conexion.close()
    return turnos
    con.close()
    return rows

def ventana_turnos_medico(parent, medico_id, solo_hoy=False):
    """
    Ventana de turnos filtrada por médico.
    - medico_id: ID del médico autenticado
    - solo_hoy: si True, muestra solo los turnos de hoy
    """
    win = tk.Toplevel(parent)
    win.title("Mis Turnos" + (" — Hoy" if solo_hoy else ""))
    win.geometry("700x400")

    columnas = ("ID", "Paciente", "Médico", "Fecha", "Hora", "Urgencia")
    tabla = ttk.Treeview(win, columns=columnas, show="headings", height=15)

    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, width=100)

    tabla.pack(fill="both", expand=True, padx=10, pady=10)

    def mostrar():
        for row in tabla.get_children():
            tabla.delete(row)
        for turno in ver_turnos(medico_id, solo_hoy=solo_hoy):
            tabla.insert("", "end", values=turno)

    tk.Button(win, text="Actualizar lista", command=mostrar).pack(pady=5)

    # mostrar al abrir
    mostrar()

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
