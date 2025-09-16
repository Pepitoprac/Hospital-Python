import tkinter as tk
from tkinter import messagebox
import sqlite3

def agregar_paciente():
    ventana = tk.Toplevel()
    ventana.title("Agregar Paciente [Panel Admin]")

    # Labels y Entrys
    tk.Label(ventana, text="DNI").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    entry_dni = tk.Entry(ventana)
    entry_dni.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(ventana, text="Nombre").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    entry_nombre = tk.Entry(ventana)
    entry_nombre.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(ventana, text="Fecha Nacimiento (YYYY-MM-DD)").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    entry_fecha = tk.Entry(ventana)
    entry_fecha.grid(row=2, column=1, padx=10, pady=5)

    # Función interna para guardar paciente
    def guardar():
        dni = entry_dni.get().strip()
        nombre = entry_nombre.get().strip()
        fecha = entry_fecha.get().strip()

        if not dni or not nombre or not fecha:
            messagebox.showwarning("Error", "Todos los campos son obligatorios")
            return

        conexion = sqlite3.connect("hospital.db")
        cursor = conexion.cursor()

        try:
            cursor.execute(
                "INSERT INTO paciente (dni, nombre, fechaNacimiento) VALUES (?, ?, ?)",
                (dni, nombre, fecha)
            )
            conexion.commit()
            messagebox.showinfo("Éxito", "Paciente agregado correctamente")

            entry_dni.delete(0, tk.END)
            entry_nombre.delete(0, tk.END)
            entry_fecha.delete(0, tk.END)

        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "El DNI ya existe")
        finally:
            conexion.close()

    # Botón
    tk.Button(ventana, text="Registrar Paciente", command=guardar).grid(row=3, column=0, columnspan=2, pady=10)
