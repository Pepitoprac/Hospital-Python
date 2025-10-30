import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from rutadb import DB as RutaDb

DB_PATH = RutaDb

# -------------------------
# Traer médicos con JOIN para mostrar nombre de especialidad
# -------------------------
def listarmedico():
    conexion = sqlite3.connect(RutaDb)
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT m.id, m.nombre, m.matricula, e.nombre as especialidad
        FROM medico m
        LEFT JOIN especialidad e ON m.especialidad_id = e.id
    """)
    medicos = cursor.fetchall()
    conexion.close()
    return medicos


# -------------------------
# Ventana Listar Médicos
# -------------------------
def ventana_listar_medicos(parent=None):
    ventana = tk.Toplevel(parent) if parent else tk.Toplevel()
    ventana.title("Lista de Médicos")
    ventana.geometry("700x400")

    columnas = ("ID", "Nombre", "Matrícula", "Especialidad")
    tabla = ttk.Treeview(ventana, columns=columnas, show="headings", height=15)

    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, anchor="center", width=160)

    tabla.pack(fill="both", expand=True, padx=10, pady=10)

    # -------------------
    # Función cargar médicos
    # -------------------
    def cargar_datos():
        for row in tabla.get_children():
            tabla.delete(row)

        medicos = listarmedico()
        if medicos:
            for medico in medicos:
                tabla.insert("", tk.END, values=medico)
        else:
            messagebox.showinfo("Sin resultados", "No hay médicos registrados en la base de datos")

    # -------------------
    # Función editar médico
    # -------------------
    def editar_medico():
        seleccionado = tabla.selection()
        if not seleccionado:
            messagebox.showwarning("Aviso", "Seleccione un médico de la tabla")
            return

        valores = tabla.item(seleccionado[0], "values")
        medico_id, nombre, matricula, especialidad_actual = valores

        ventana_edit = tk.Toplevel(ventana)
        ventana_edit.title(f"Editar Médico ID {medico_id}")
        ventana_edit.geometry("400x250")

        tk.Label(ventana_edit, text="Nombre").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        entry_nombre = tk.Entry(ventana_edit)
        entry_nombre.insert(0, nombre)
        entry_nombre.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(ventana_edit, text="Matrícula").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        entry_matricula = tk.Entry(ventana_edit)
        entry_matricula.insert(0, matricula)
        entry_matricula.grid(row=1, column=1, padx=10, pady=5)

        # Traer lista de especialidades
        conexion = sqlite3.connect(RutaDb)
        cursor = conexion.cursor()
        cursor.execute("SELECT id, nombre FROM especialidad")
        especialidades = cursor.fetchall()
        conexion.close()

        tk.Label(ventana_edit, text="Especialidad").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        combo_especialidad = ttk.Combobox(ventana_edit, values=[e[1] for e in especialidades])
        combo_especialidad.set(especialidad_actual)  # preselecciona la actual
        combo_especialidad.grid(row=2, column=1, padx=10, pady=5)

        # Guardar cambios
        def guardar_cambios():
            nuevo_nombre = entry_nombre.get().strip()
            nueva_matricula = entry_matricula.get().strip()
            nueva_esp = combo_especialidad.get().strip()

            if not nuevo_nombre or not nueva_matricula or not nueva_esp:
                messagebox.showwarning("Error", "Todos los campos son obligatorios")
                return

            # Buscar id de especialidad
            esp_id = None
            for e in especialidades:
                if e[1] == nueva_esp:
                    esp_id = e[0]
                    break

            conexion = sqlite3.connect(RutaDb)
            cursor = conexion.cursor()
            cursor.execute("""
                UPDATE medico
                SET nombre = ?, matricula = ?, especialidad_id = ?
                WHERE id = ?
            """, (nuevo_nombre, nueva_matricula, esp_id, medico_id))
            conexion.commit()
            conexion.close()

            messagebox.showinfo("Éxito", "Médico actualizado correctamente")
            ventana_edit.destroy()
            cargar_datos()

        tk.Button(ventana_edit, text="Guardar", command=guardar_cambios, bg="lightgreen").grid(row=3, column=0, columnspan=2, pady=15)

    # -------------------
    # Botones de acción
    # -------------------
    tk.Button(ventana, text="Actualizar Lista", command=cargar_datos, bg="lightblue").pack(pady=5)
    tk.Button(ventana, text="Editar Médico", command=editar_medico, bg="lightyellow").pack(pady=5)

    cargar_datos()

