import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

DB_PATH = "hospital.db"

# -------------------------
# Traer pacientes
# -------------------------
def listarpaciente():
    with sqlite3.connect(DB_PATH, timeout=10) as conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT id, dni, nombre, fechaNacimiento, urgencia FROM paciente")
        pacientes = cursor.fetchall()
    return pacientes


# -------------------------
# Ventana Listar Pacientes
# -------------------------
def ventana_listar_pacientes():
    ventana = tk.Toplevel()
    ventana.title("Lista de Pacientes")
    ventana.geometry("750x400")

    columnas = ("ID", "DNI", "Nombre", "Fecha Nacimiento", "Urgencia")
    tabla = ttk.Treeview(ventana, columns=columnas, show="headings", height=15)

    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, anchor="center", width=140)

    tabla.pack(fill="both", expand=True, padx=10, pady=10)

    # -------------------
    # Cargar pacientes
    # -------------------
    def cargar_datos():
        for row in tabla.get_children():
            tabla.delete(row)

        pacientes = listarpaciente()
        if pacientes:
            for paciente in pacientes:
                tabla.insert("", tk.END, values=paciente)
        else:
            messagebox.showinfo("Sin resultados", "No hay pacientes registrados en la base de datos")

    # -------------------
    # Editar urgencia
    # -------------------
    def editar_urgencia():
        seleccionado = tabla.selection()
        if not seleccionado:
            messagebox.showwarning("Aviso", "Seleccione un paciente de la tabla")
            return

        valores = tabla.item(seleccionado[0], "values")
        paciente_id, dni, nombre, fechaNac, urgencia = valores

        ventana_edit = tk.Toplevel(ventana)
        ventana_edit.title(f"Asignar Urgencia - {nombre}")
        ventana_edit.geometry("300x150")

        tk.Label(ventana_edit, text="Nivel de Urgencia (1-5):").pack(pady=10)
        entry_urgencia = tk.Entry(ventana_edit)
        entry_urgencia.pack(pady=5)
        entry_urgencia.insert(0, urgencia if urgencia else "")

        def guardar():
            nueva_urgencia = entry_urgencia.get().strip()
            if not nueva_urgencia.isdigit() or not (1 <= int(nueva_urgencia) <= 5):
                messagebox.showerror("Error", "La urgencia debe ser un número entre 1 y 5")
                return

            try:
                with sqlite3.connect(DB_PATH, timeout=10) as conexion:
                    cursor = conexion.cursor()
                    cursor.execute(
                        "UPDATE paciente SET urgencia = ? WHERE id = ?",
                        (nueva_urgencia, paciente_id)
                    )
                    conexion.commit()

                messagebox.showinfo("Éxito", "Urgencia actualizada correctamente")
                ventana_edit.destroy()
                cargar_datos()
            except sqlite3.OperationalError as e:
                messagebox.showerror("Error", f"No se pudo actualizar: {e}")

        tk.Button(ventana_edit, text="Guardar", command=guardar, bg="lightgreen").pack(pady=10)

    # -------------------
    # Botones
    # -------------------
    tk.Button(ventana, text="Actualizar Lista", command=cargar_datos, bg="lightblue").pack(pady=5)
    tk.Button(ventana, text="Asignar Urgencia", command=editar_urgencia, bg="lightyellow").pack(pady=5)

    cargar_datos()

