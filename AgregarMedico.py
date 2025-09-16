import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

def agregarmedico():
    ventana = tk.Toplevel()
    ventana.title("Agregar Médico [Panel Admin]")

    # Labels y Entrys
    tk.Label(ventana, text="Nombre").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    entry_nombre = tk.Entry(ventana)
    entry_nombre.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(ventana, text="Matrícula").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    entry_matricula = tk.Entry(ventana)
    entry_matricula.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(ventana, text="Especialidad").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    combo_especialidad = ttk.Combobox(ventana, state="readonly", width=27)
    combo_especialidad.grid(row=2, column=1, padx=10, pady=5)

    # --- Cargar especialidades desde la DB ---
    conexion = sqlite3.connect("hospital.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre FROM especialidad")
    especialidades = cursor.fetchall()  # [(1, 'Cardiología'), (2, 'Pediatría'), ...]
    conexion.close()

    # Guardamos en un diccionario { "Cardiología": 1, ... } para obtener el ID después
    esp_dict = {nombre: id_ for id_, nombre in especialidades}
    combo_especialidad["values"] = list(esp_dict.keys())

    # Función interna para guardar médico
    def guardar():
        nombre = entry_nombre.get().strip()
        matricula = entry_matricula.get().strip()
        esp_nombre = combo_especialidad.get().strip()

        if not nombre or not matricula or not esp_nombre:
            messagebox.showwarning("Error", "Todos los campos son obligatorios")
            return

        especialidad_id = esp_dict[esp_nombre]

        conexion = sqlite3.connect("hospital.db")
        cursor = conexion.cursor()

        try:
            cursor.execute(
                "INSERT INTO medico (nombre, matricula, especialidad_id) VALUES (?, ?, ?)",
                (nombre, matricula, especialidad_id)
            )
            conexion.commit()
            messagebox.showinfo("Éxito", "Médico agregado correctamente")

            entry_nombre.delete(0, tk.END)
            entry_matricula.delete(0, tk.END)
            combo_especialidad.set("")

        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "La matrícula ya existe o la especialidad no es válida")
        finally:
            conexion.close()

    # Botón
    tk.Button(ventana, text="Registrar Médico", command=guardar).grid(row=3, column=0, columnspan=2, pady=10)
    