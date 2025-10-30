import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from rutadb import DB as RutaDb

DB_PATH = RutaDb

def historialporpaciente(parent=None):
    ventana = tk.Toplevel(parent) if parent else tk.Toplevel()

    def buscar():
        dni = entry_dni.get().strip()
        if not dni:
            messagebox.showwarning("Error", "Ingrese un DNI.")
            return

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                p.nombre, 
                hc.fecha, 
                hc.hora, 
                a.descripcion AS area, 
                m.nombre AS medico, 
                hc.detalles_sintomas
            FROM historia_clinica hc
            JOIN paciente p ON p.id = hc.paciente_id
            LEFT JOIN medico m ON m.id = hc.medico_id
            LEFT JOIN area a ON a.id = hc.area_id
            WHERE p.dni = ?
            ORDER BY hc.fecha DESC, hc.hora DESC
        """, (dni,))
        resultados = cursor.fetchall()
        conn.close()

        for row in tabla.get_children():
            tabla.delete(row)

        if resultados:
            for r in resultados:
                tabla.insert("", "end", values=r)
        else:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT nombre FROM paciente WHERE dni = ?", (dni,))
            paciente = cursor.fetchone()
            conn.close()

            if paciente:
                messagebox.showinfo("Sin historias", f"El paciente '{paciente[0]}' no tiene historias clínicas aún.")
            else:
                messagebox.showinfo("Sin resultados", f"No se encontró ningún paciente con DNI: {dni}")

    ventana = tk.Toplevel()
    ventana.title("Historial por Paciente")
    ventana.geometry("900x400")

    tk.Label(ventana, text="DNI del paciente:").pack(pady=5)
    entry_dni = tk.Entry(ventana)
    entry_dni.pack(pady=5)

    tk.Button(ventana, text="Buscar", command=buscar, bg="lightblue").pack(pady=5)

    columnas = ("Paciente", "Fecha", "Hora", "Área", "Médico", "Síntomas")
    tabla = ttk.Treeview(ventana, columns=columnas, show="headings", height=10)

    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, anchor="center", width=140)

    tabla.pack(fill="both", expand=True, padx=10, pady=10)
