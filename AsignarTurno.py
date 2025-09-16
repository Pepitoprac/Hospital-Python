import tkinter as tk
from tkinter import messagebox
import sqlite3

def asignarturno():
    ventana = tk.Toplevel()
    ventana.title("Asignar Turno [Panel Admin]")

    # -----------------------------
    # Campos del formulario
    # -----------------------------
    tk.Label(ventana, text="ID Paciente").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    entry_paciente = tk.Entry(ventana)
    entry_paciente.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(ventana, text="ID Médico").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    entry_medico = tk.Entry(ventana)
    entry_medico.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(ventana, text="Fecha (YYYY-MM-DD)").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    entry_fecha = tk.Entry(ventana)
    entry_fecha.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(ventana, text="Hora (HH:MM)").grid(row=3, column=0, padx=10, pady=5, sticky="w")
    entry_hora = tk.Entry(ventana)
    entry_hora.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(ventana, text="Urgencia (0/1)").grid(row=4, column=0, padx=10, pady=5, sticky="w")
    entry_urgencia = tk.Entry(ventana)
    entry_urgencia.grid(row=4, column=1, padx=10, pady=5)

    tk.Label(ventana, text="ID Área").grid(row=5, column=0, padx=10, pady=5, sticky="w")
    entry_area = tk.Entry(ventana)
    entry_area.grid(row=5, column=1, padx=10, pady=5)

    # -----------------------------
    # Función para guardar turno
    # -----------------------------
    def guardar():
        paciente = entry_paciente.get().strip()
        medico = entry_medico.get().strip()
        fecha = entry_fecha.get().strip()
        hora = entry_hora.get().strip()
        urgencia = entry_urgencia.get().strip()
        area = entry_area.get().strip()

        if not paciente or not medico or not fecha or not hora or not urgencia or not area:
            messagebox.showwarning("Error", "Todos los campos son obligatorios")
            return

        conexion = sqlite3.connect("hospital.db")
        cursor = conexion.cursor()
        try:
            cursor.execute("""
                INSERT INTO turno (paciente_id, medico_id, fecha, hora, urgencia, area_id)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (paciente, medico, fecha, hora, urgencia, area))
            conexion.commit()
            messagebox.showinfo("Éxito", "Turno asignado correctamente")

            # Limpio los campos
            entry_paciente.delete(0, tk.END)
            entry_medico.delete(0, tk.END)
            entry_fecha.delete(0, tk.END)
            entry_hora.delete(0, tk.END)
            entry_urgencia.delete(0, tk.END)
            entry_area.delete(0, tk.END)

        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Error al asignar el turno. Verifique los datos.")
        finally:
            conexion.close()

    # -----------------------------
    # Botón Confirmar Turno
    # -----------------------------
    tk.Button(ventana, text="Confirmar Turno", command=guardar, bg="lightgreen").grid(
        row=6, column=0, columnspan=2, pady=10
    )
