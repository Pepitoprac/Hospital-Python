import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

# -------------------------
# Función historial paciente
# -------------------------
def historialporpaciente(paciente_id):
    conexion = sqlite3.connect("hospital.db")
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT hc.id, hc.fecha, hc.hora, hc.detalles_sintomas, m.nombre, a.descripcion
        FROM historia_clinica hc
        JOIN medico m ON hc.medico_id = m.id
        JOIN area a ON hc.area_id = a.id
        WHERE hc.paciente_id = ?
    """, (paciente_id,))
    historial = cursor.fetchall()
    conexion.close()
    return historial


# -------------------------
# Interfaz Tkinter
# -------------------------
def ventana_historialpaciente():
    ventana = tk.Toplevel()
    ventana.title("Historial por Paciente")

    # Label y campo de entrada
    tk.Label(ventana, text="ID Paciente").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    entry_paciente = tk.Entry(ventana)
    entry_paciente.grid(row=0, column=1, padx=10, pady=5)

    # Treeview para mostrar resultados
    columnas = ("ID", "Fecha", "Hora", "Síntomas", "Médico", "Área")
    tabla = ttk.Treeview(ventana, columns=columnas, show="headings", height=10)

    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, anchor="center", width=120)

    tabla.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    # Función que se ejecuta al presionar el botón
    def mostrar():
        paciente_id = entry_paciente.get().strip()
        if not paciente_id:
            messagebox.showwarning("Error", "Debe ingresar el ID del paciente")
            return

        historial = historialporpaciente(paciente_id)

        # Limpiar tabla antes de insertar
        for row in tabla.get_children():
            tabla.delete(row)

        if historial:
            for fila in historial:
                tabla.insert("", tk.END, values=fila)
        else:
            messagebox.showinfo("Sin resultados", "No se encontró historial para este paciente")

    # Botón buscar
    tk.Button(
        ventana,
        text="Buscar Historial",
        command=mostrar,
        bg="lightblue"
    ).grid(row=1, column=0, columnspan=2, pady=10)
