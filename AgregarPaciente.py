import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from tkcalendar import DateEntry  # <-- Importar
from datetime import datetime

def agregar_paciente():
    ventana = tk.Toplevel()
    ventana.title("Agregar Paciente [Panel Admin]")

    # -------------------------
    # Campos del formulario
    # -------------------------
    tk.Label(ventana, text="DNI").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    entry_dni = tk.Entry(ventana)
    entry_dni.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(ventana, text="Nombre").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    entry_nombre = tk.Entry(ventana)
    entry_nombre.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(ventana, text="Fecha Nacimiento").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    entry_fecha = DateEntry(ventana, date_pattern="yyyy-mm-dd")  # <-- Calendario
    entry_fecha.grid(row=2, column=1, padx=10, pady=5)

    # -------------------------
    # Urgencia (Combobox 1–4)
    # -------------------------
    tk.Label(ventana, text="Urgencia").grid(row=3, column=0, padx=10, pady=5, sticky="w")

    urgencia_map = {
        "1 - Leve": 1,
        "2 - Moderada": 2,
        "3 - Grave": 3,
        "4 - Crítica": 4
    }

    combo_urgencia = ttk.Combobox(ventana, state="readonly", width=20)
    combo_urgencia["values"] = list(urgencia_map.keys())
    combo_urgencia.grid(row=3, column=1, padx=10, pady=5)
    combo_urgencia.set(list(urgencia_map.keys())[0])  # Valor por defecto

    # -------------------------
    # Guardar paciente
    # -------------------------
    def guardar():
        dni = entry_dni.get().strip()
        nombre = entry_nombre.get().strip()
        fecha = entry_fecha.get_date().strftime("%Y-%m-%d")  # <-- Obtenemos la fecha del calendario
        urgencia_sel = combo_urgencia.get().strip()

        # Validaciones
        if len(dni) != 8 or not dni.isdigit():
            messagebox.showerror("Error", "¡El DNI debe tener 8 dígitos!")
            return

        if not nombre or not urgencia_sel:
            messagebox.showwarning("Error", "Todos los campos son obligatorios")
            return

        urgencia_valor = urgencia_map[urgencia_sel]

        conexion = sqlite3.connect("hospital.db")
        cursor = conexion.cursor()

        try:
            cursor.execute(
                "INSERT INTO paciente (dni, nombre, fechaNacimiento, urgencia) VALUES (?, ?, ?, ?)",
                (dni, nombre, fecha, urgencia_valor)
            )
            conexion.commit()
            messagebox.showinfo("Éxito", "Paciente agregado correctamente")

            # Limpiar campos
            entry_dni.delete(0, tk.END)
            entry_nombre.delete(0, tk.END)
            entry_fecha.set_date(datetime.today())
            combo_urgencia.set(list(urgencia_map.keys())[0])

        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "El DNI ya existe")
        finally:
            conexion.close()

    # -------------------------
    # Botón Registrar
    # -------------------------
    tk.Button(ventana, text="Registrar Paciente", command=guardar, bg="lightgreen").grid(
        row=4, column=0, columnspan=2, pady=10
    )
