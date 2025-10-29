import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from rutadb import DB as RutaDb

DB_PATH = RutaDb

def agregarmedico(parent=None):
    ventana = tk.Toplevel(parent) if parent else tk.Tk()
    ventana.title("Registrar Médico")
    ventana.geometry("420x300")
    ventana.resizable(False, False)

    # ===== Etiquetas y entradas =====
    tk.Label(ventana, text="Nombre del médico:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    entry_nombre = tk.Entry(ventana, width=30)
    entry_nombre.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(ventana, text="Matrícula:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    entry_matricula = tk.Entry(ventana, width=30)
    entry_matricula.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(ventana, text="Contraseña:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    entry_contrasena = tk.Entry(ventana, width=30, show="*")
    entry_contrasena.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(ventana, text="Especialidad:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
    combo_especialidad = ttk.Combobox(ventana, state="readonly", width=28)
    combo_especialidad.grid(row=3, column=1, padx=10, pady=5)

    # ===== Cargar especialidades =====
    try:
        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()
        cursor.execute("SELECT id, nombre FROM especialidad ORDER BY nombre")
        especialidades = cursor.fetchall()
    except Exception as e:
        messagebox.showerror("Error DB", f"No se pudieron cargar las especialidades:\n{e}")
        return
    finally:
        try: conexion.close()
        except: pass

    if especialidades:
        esp_dict = {nombre: id_ for id_, nombre in especialidades}
        combo_especialidad["values"] = list(esp_dict.keys())
        combo_especialidad.set("Seleccionar especialidad")
    else:
        messagebox.showwarning("Atención", "No hay especialidades cargadas en la base de datos.")
        esp_dict = {}

    # ===== Guardar médico y usuario =====
    def guardar():
        nombre = entry_nombre.get().strip()
        matricula = entry_matricula.get().strip()
        contrasena = entry_contrasena.get().strip()
        esp_nombre = combo_especialidad.get().strip()

        if not nombre or not matricula or not contrasena or esp_nombre == "Seleccionar especialidad":
            messagebox.showwarning("Campos vacíos", "Todos los campos son obligatorios.")
            return

        especialidad_id = esp_dict.get(esp_nombre)
        if not especialidad_id:
            messagebox.showerror("Error", "Seleccione una especialidad válida.")
            return

        try:
            conexion = sqlite3.connect(DB_PATH)
            cursor = conexion.cursor()

            # Verificar duplicados
            cursor.execute("SELECT id FROM medico WHERE matricula = ?", (matricula,))
            if cursor.fetchone():
                messagebox.showerror("Error", "Ya existe un médico con esa matrícula.")
                return

            # Insertar el médico
            cursor.execute("""
                INSERT INTO medico (nombre, matricula, especialidad_id)
                VALUES (?, ?, ?)
            """, (nombre, matricula, especialidad_id))
            medico_id = cursor.lastrowid

            # Crear usuario médico
            cursor.execute("""
                INSERT INTO usuario (nombre, contrasena, rol, medico_id)
                VALUES (?, ?, 'medico', ?)
            """, (nombre, contrasena, medico_id))

            conexion.commit()
        except Exception as e:
            messagebox.showerror("Error al guardar", f"No se pudo registrar el médico:\n{e}")
            return
        finally:
            conexion.close()

        messagebox.showinfo("Éxito", f"Médico '{nombre}' y su usuario fueron creados correctamente.")
        entry_nombre.delete(0, tk.END)
        entry_matricula.delete(0, tk.END)
        entry_contrasena.delete(0, tk.END)
        combo_especialidad.set("Seleccionar especialidad")

    tk.Button(ventana, text="Registrar Médico", command=guardar, bg="lightgreen").grid(
        row=5, column=0, columnspan=2, pady=15
    )

    if parent is None:
        ventana.mainloop()
