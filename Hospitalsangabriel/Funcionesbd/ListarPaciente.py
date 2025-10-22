import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from rutadb import DB as RutaDb

DB_PATH = RutaDb

# -------------------------
# Traer pacientes
# -------------------------
def listarpaciente():
    with sqlite3.connect(DB_PATH, timeout=10) as conexion:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT id, dni, nombre, fechaNacimiento
            FROM paciente
            ORDER BY id
        """)
        pacientes = cursor.fetchall()
    return pacientes


# -------------------------
# Ventana Listar Pacientes
# -------------------------
def ventana_listar_pacientes():
    ventana = tk.Toplevel()
    ventana.title("Lista de Pacientes")
    ventana.geometry("650x400")

    columnas = ("ID", "DNI", "Nombre", "Fecha Nacimiento")
    tabla = ttk.Treeview(ventana, columns=columnas, show="headings", height=15)

    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, anchor="center", width=150)

    tabla.pack(fill="both", expand=True, padx=10, pady=10)

    # -------------------
    # Cargar pacientes
    # -------------------
    def cargar_datos():
        # Limpiar tabla antes de volver a cargar
        for row in tabla.get_children():
            tabla.delete(row)

        pacientes = listarpaciente()
        if pacientes:
            for paciente in pacientes:
                tabla.insert("", tk.END, values=paciente)
        else:
            messagebox.showinfo("Sin resultados", "No hay pacientes registrados en la base de datos.")

    # -------------------
    # Botón actualizar lista
    # -------------------
    boton_frame = tk.Frame(ventana)
    boton_frame.pack(pady=5)

    tk.Button(
        boton_frame,
        text="Actualizar Lista",
        command=cargar_datos,
        bg="lightblue",
        width=20
    ).grid(row=0, column=0, padx=5)

    cargar_datos()
