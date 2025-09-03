import tkinter as tk
from tkinter import messagebox
from Modelos.Paciente import Paciente
import sqlite3

def agregar_paciente(Paciente):
    dni = entry_dni.get()
    nombre = entry_nombre.get()
    fecha = entry_fecha.get()
    
    if not dni or not nombre or not fecha:
        messagebox.showwarning("Error", "Todos los campos son obligatorios")
        return
    
    conexion = sqlite3.connect("hospital.db")
    cursor = conexion.cursor()
    
    try:
        cursor.execute("INSERT INTO paciente (dni, nombre, fechaNacimiento) VALUES (?, ?, ?)", 
                       (dni, nombre, fecha))
        conexion.commit()
        messagebox.showinfo("Éxito", "Paciente agregado correctamente")
        entry_dni.delete(0, tk.END)
        entry_nombre.delete(0, tk.END)
        entry_fecha.delete(0, tk.END)
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "El DNI ya existe")
    finally:
        conexion.close()

# Ventana principal
root = tk.Tk()
root.title("Agregar Paciente")

tk.Label(root, text="DNI").grid(row=0, column=0)
entry_dni = tk.Entry(root)
entry_dni.grid(row=0, column=1)

tk.Label(root, text="Nombre").grid(row=1, column=0)
entry_nombre = tk.Entry(root)
entry_nombre.grid(row=1, column=1)

tk.Label(root, text="Fecha Nacimiento (YYYY-MM-DD)").grid(row=2, column=0)
entry_fecha = tk.Entry(root)
entry_fecha.grid(row=2, column=1)

tk.Button(root, text="Agregar Paciente", command=agregar_paciente).grid(row=3, column=0, columnspan=2)

root.mainloop()
