# agregar_historia_clinica.py
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

DB_PATH = "hospital.db"

def agregar_historia_clinica(medico_logueado):
    """
    medico_logueado: dict con al menos {"id": int, "nombre": str}
    """
    ventana = tk.Toplevel()
    ventana.title("Agregar Historia Clínica")
    ventana.geometry("500x450")

    # --- Cargar datos de la DB ---
    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()

    cursor.execute("SELECT id, nombre FROM paciente")
    pacientes = cursor.fetchall()
    pacientes_map = {f"{p[1]} (ID:{p[0]})": p[0] for p in pacientes}

    cursor.execute("SELECT id, descripcion FROM area")
    areas = cursor.fetchall()
    areas_map = {f"{a[1]} (ID:{a[0]})": a[0] for a in areas}

    cursor.execute("SELECT id, nombre FROM medico")
    medicos = cursor.fetchall()
    medicos_map = {f"{m[1]} (ID:{m[0]})": m[0] for m in medicos}

    conexion.close()

    # --- Paciente ---
    tk.Label(ventana, text="Paciente").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    pacientes_combo = ttk.Combobox(ventana, state="readonly", values=list(pacientes_map.keys()))
    pacientes_combo.grid(row=0, column=1, padx=10, pady=5)
    if pacientes_combo["values"]:
        pacientes_combo.set(pacientes_combo["values"][0])

    # --- Área ---
    tk.Label(ventana, text="Área").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    areas_combo = ttk.Combobox(ventana, state="readonly", values=list(areas_map.keys()))
    areas_combo.grid(row=1, column=1, padx=10, pady=5)
    if areas_combo["values"]:
        areas_combo.set(areas_combo["values"][0])

    # --- Médico (selección) ---
    tk.Label(ventana, text="Médico").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    medicos_combo = ttk.Combobox(ventana, state="readonly", values=list(medicos_map.keys()))
    medicos_combo.grid(row=2, column=1, padx=10, pady=5)
    # Por defecto se selecciona el médico logueado
    med_default = next((k for k, v in medicos_map.items() if v == medico_logueado["id"]), None)
    if med_default:
        medicos_combo.set(med_default)
    elif medicos_combo["values"]:
        medicos_combo.set(medicos_combo["values"][0])

    # --- Fecha y Hora ---
    tk.Label(ventana, text="Fecha (YYYY-MM-DD)").grid(row=3, column=0, padx=10, pady=5, sticky="w")
    entry_fecha = tk.Entry(ventana)
    entry_fecha.grid(row=3, column=1, padx=10, pady=5)
    entry_fecha.insert(0, datetime.today().strftime("%Y-%m-%d"))

    tk.Label(ventana, text="Hora (HH:MM)").grid(row=4, column=0, padx=10, pady=5, sticky="w")
    entry_hora = tk.Entry(ventana)
    entry_hora.grid(row=4, column=1, padx=10, pady=5)
    entry_hora.insert(0, datetime.now().strftime("%H:%M"))

    # --- Detalles / Síntomas ---
    tk.Label(ventana, text="Detalles / Síntomas").grid(row=5, column=0, padx=10, pady=5, sticky="nw")
    txt_frame = tk.Frame(ventana)
    txt_frame.grid(row=5, column=1, padx=10, pady=5)
    txt_detalles = tk.Text(txt_frame, width=35, height=8, wrap="word")
    txt_detalles.pack(side="left", fill="y")
    scrollbar = ttk.Scrollbar(txt_frame, orient="vertical", command=txt_detalles.yview)
    scrollbar.pack(side="right", fill="y")
    txt_detalles.config(yscrollcommand=scrollbar.set)

    # --- Botón Guardar ---
    def guardar():
        paciente_sel = pacientes_combo.get()
        area_sel = areas_combo.get()
        medico_sel = medicos_combo.get()
        fecha = entry_fecha.get().strip()
        hora = entry_hora.get().strip()
        detalles = txt_detalles.get("1.0", tk.END).strip()

        if not paciente_sel or not area_sel or not medico_sel or not fecha or not hora:
            messagebox.showwarning("Error", "Todos los campos son obligatorios")
            return

        # Validar fecha
        try:
            datetime.strptime(fecha, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Fecha inválida. Formato YYYY-MM-DD")
            return

        # Validar hora
        try:
            datetime.strptime(hora, "%H:%M")
        except ValueError:
            messagebox.showerror("Error", "Hora inválida. Formato HH:MM")
            return

        paciente_id = pacientes_map[paciente_sel]
        area_id = areas_map[area_sel]
        medico_id = medicos_map[medico_sel]

        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()
        try:
            cursor.execute(
                "INSERT INTO historia_clinica (paciente_id, medico_id, area_id, fecha, hora, detalles_sintomas) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (paciente_id, medico_id, area_id, fecha, hora, detalles)
            )
            conexion.commit()
            messagebox.showinfo("Éxito", f"Historia clínica creada por {medico_sel}")
            ventana.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear la historia clínica:\n{e}")
        finally:
            conexion.close()

    tk.Button(ventana, text="Guardar Historia Clínica", command=guardar, bg="lightgreen").grid(
        row=6, column=0, columnspan=2, pady=10
    )
