import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from rutadb import DB as RutaDb

DB_PATH = RutaDb
# -------------------------
# Traer pacientes
# -------------------------
def listarpaciente():
    with sqlite3.connect(DB_PATH, timeout=10) as conexion:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT id, dni, nombre, fechaNacimiento, urgencia
            FROM paciente
            ORDER BY id
        """)
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
                # Si no tiene urgencia, mostrar guion
                id, dni, nombre, fecha, urgencia = paciente
                urgencia = urgencia if urgencia is not None else "—"
                tabla.insert("", tk.END, values=(id, dni, nombre, fecha, urgencia))
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
        ventana_edit.geometry("300x180")

        tk.Label(ventana_edit, text="Nivel de Urgencia (1: Baja | 2: Media | 3: Alta)").pack(pady=10)

        # Combobox en lugar de Entry
        opciones_urgencia = ["1", "2", "3"]
        combo_urgencia = ttk.Combobox(ventana_edit, values=opciones_urgencia, state="readonly")
        combo_urgencia.pack(pady=5)
        if urgencia in opciones_urgencia:
            combo_urgencia.set(urgencia)

        def guardar():
            nueva_urgencia = combo_urgencia.get().strip()
            if nueva_urgencia not in ["1", "2", "3"]:
                messagebox.showerror("Error", "Seleccione una urgencia válida (1, 2 o 3)")
                return

            try:
                with sqlite3.connect(RutaDb, timeout=10) as conexion:
                    cursor = conexion.cursor()
                    cursor.execute(
                        "UPDATE paciente SET urgencia = ? WHERE id = ?",
                        (int(nueva_urgencia), paciente_id)
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
    boton_frame = tk.Frame(ventana)
    boton_frame.pack(pady=5)

    tk.Button(boton_frame, text="Actualizar Lista", command=cargar_datos, bg="lightblue", width=18).grid(row=0, column=0, padx=5)
    tk.Button(boton_frame, text="Asignar Urgencia", command=editar_urgencia, bg="lightyellow", width=18).grid(row=0, column=1, padx=5)

    cargar_datos()
