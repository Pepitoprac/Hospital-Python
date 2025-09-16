import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# --------------------
# Función listar médico
# --------------------
def listarmedico():
    conexion = sqlite3.connect("hospital.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre, matricula, especialidad_id FROM medico")
    medicos = cursor.fetchall()
    conexion.close()
    return medicos


# --------------------
# Interfaz Tkinter
# --------------------
def ventana_listar_medicos():
    ventana = tk.Toplevel()
    ventana.title("Lista de Médicos")
    ventana.geometry("600x400")

    # Tabla
    columnas = ("ID", "Nombre", "Matrícula", "Especialidad ID")
    tabla = ttk.Treeview(ventana, columns=columnas, show="headings", height=15)

    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, anchor="center", width=140)

    tabla.pack(fill="both", expand=True, padx=10, pady=10)

    # Botón actualizar
    def cargar_datos():
        for row in tabla.get_children():
            tabla.delete(row)

        medicos = listarmedico()
        if medicos:
            for medico in medicos:
                tabla.insert("", tk.END, values=medico)
        else:
            messagebox.showinfo("Sin resultados", "No hay médicos registrados en la base de datos")

    btn_actualizar = tk.Button(ventana, text="Actualizar Lista", command=cargar_datos, bg="lightblue")
    btn_actualizar.pack(pady=5)

    # Cargar datos automáticamente al abrir
    cargar_datos()
