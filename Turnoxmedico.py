import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

DB_PATH = "hospital.db"

# --------------------
# Obtener médicos (id, matricula, nombre)
# --------------------
def obtener_medicos():
    with sqlite3.connect(DB_PATH) as conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT id, matricula, nombre FROM medico")
        return cursor.fetchall()

# --------------------
# Ver turnos por médico
# --------------------
def verturnopormedico(medico_id):
    with sqlite3.connect(DB_PATH) as conexion:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT t.id, p.nombre, t.fecha, t.hora, t.urgencia
            FROM turno t
            JOIN paciente p ON t.paciente_id = p.id
            WHERE t.medico_id = ?
            ORDER BY t.urgencia DESC, t.fecha, t.hora
        """, (medico_id,))
        return cursor.fetchall()

# --------------------
# Ventana Tkinter
# --------------------
def ventana_turnos_por_medico():
    ventana = tk.Toplevel()
    ventana.title("Turnos por Médico")
    ventana.geometry("800x450")

    # Selector de médico
    tk.Label(ventana, text="Seleccione un médico:").pack(pady=5)
    medicos = obtener_medicos()
    if not medicos:
        messagebox.showwarning("Aviso", "No hay médicos registrados en la base de datos")
        ventana.destroy()
        return

    # Mapeo para identificar ID del médico según la selección
    medico_map = {f"{m[1]} - {m[2]}": m[0] for m in medicos}

    combo_medico = ttk.Combobox(ventana, values=list(medico_map.keys()), state="readonly", width=50)
    combo_medico.pack(pady=5)

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

        seleccionado = combo_medico.get()
        if not seleccionado:
            messagebox.showwarning("Aviso", "Seleccione un médico")
            return

        medico_id = medico_map[seleccionado]
        turnos = verturnopormedico(medico_id)

        if turnos:
            for turno in turnos:
                tabla.insert("", tk.END, values=turno)
        else:
            messagebox.showinfo("Sin turnos", f"El médico {seleccionado} no tiene turnos registrados")

    # Botón consultar
    tk.Button(ventana, text="Ver Turnos", command=cargar_turnos, bg="lightblue").pack(pady=5)

    # Botón actualizar
    tk.Button(ventana, text="Actualizar", command=cargar_turnos, bg="lightgreen").pack(pady=5)

