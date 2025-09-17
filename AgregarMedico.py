import os
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

    # --- Ruta absoluta del DB ---
    db_path = os.path.abspath("hospital.db")

    # --- Cargar especialidades desde la DB ---
    try:
        conexion = sqlite3.connect(db_path)
        cursor = conexion.cursor()
        cursor.execute("SELECT id, nombre FROM especialidad ORDER BY nombre")
        especialidades = cursor.fetchall()
    except Exception as e:
        messagebox.showerror("Error DB", f"No se pudo leer la tabla 'especialidad'.\nRuta DB: {db_path}\n\n{e}")
        return
    finally:
        try:
            conexion.close()
        except:
            pass

    if not especialidades:
        messagebox.showwarning("Sin especialidades",
            f"No se encontraron especialidades en la base de datos.\nDB: {db_path}")
        combo_especialidad["values"] = []
        esp_dict = {}
    else:
        # Diccionario { "Cardiología": 1, "Pediatría": 2, ... }
        esp_dict = {nombre: id_ for id_, nombre in especialidades}
        combo_especialidad["values"] = list(esp_dict.keys())
        combo_especialidad.set("Seleccionar especialidad")

    # --- Función para guardar médico ---
    def guardar():
        nombre = entry_nombre.get().strip()
        matricula = entry_matricula.get().strip()
        esp_nombre = combo_especialidad.get().strip()

        if not nombre or not matricula or not esp_nombre or esp_nombre == "Seleccionar especialidad":
            messagebox.showwarning("Error", "Todos los campos son obligatorios")
            return

        if esp_nombre not in esp_dict:
            messagebox.showerror("Error", "Especialidad inválida. Seleccioná una opción de la lista.")
            return

        especialidad_id = esp_dict[esp_nombre]

        try:
            conexion = sqlite3.connect(db_path)
            cursor = conexion.cursor()
            cursor.execute(
                "INSERT INTO medico (nombre, matricula, especialidad_id) VALUES (?, ?, ?)",
                (nombre, matricula, especialidad_id)
            )
            conexion.commit()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "La matrícula ya existe o la especialidad no es válida")
            return
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el médico:\n{e}")
            return
        finally:
            try:
                conexion.close()
            except:
                pass

        messagebox.showinfo("Éxito", "Médico agregado correctamente")
        entry_nombre.delete(0, tk.END)
        entry_matricula.delete(0, tk.END)
        combo_especialidad.set("Seleccionar especialidad")

    # Botón
    tk.Button(ventana, text="Registrar Médico", command=guardar).grid(row=3, column=0, columnspan=2, pady=10)
