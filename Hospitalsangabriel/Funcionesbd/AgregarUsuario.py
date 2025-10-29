import tkinter as tk
from tkinter import messagebox
import sqlite3
from rutadb import DB as RutaDb

DB_PATH = RutaDb

def agregarusuario_admin(parent=None):
    ventana = tk.Toplevel(parent) if parent else tk.Tk()
    ventana.title("Registrar Usuario Administrador")
    ventana.geometry("400x250")
    ventana.resizable(False, False)

    # Campos
    tk.Label(ventana, text="Nombre de usuario:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    entry_nombre = tk.Entry(ventana, width=30)
    entry_nombre.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(ventana, text="Contraseña:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    entry_contrasena = tk.Entry(ventana, width=30, show="*")
    entry_contrasena.grid(row=1, column=1, padx=10, pady=5)

    # Función para guardar
    def guardar():
        nombre = entry_nombre.get().strip()
        contrasena = entry_contrasena.get().strip()

        if not nombre or not contrasena:
            messagebox.showwarning("Campos vacíos", "Debe completar todos los campos.")
            return

        try:
            conexion = sqlite3.connect(DB_PATH)
            cursor = conexion.cursor()

            # Verificar duplicado
            cursor.execute("SELECT id FROM usuario WHERE nombre = ?", (nombre,))
            if cursor.fetchone():
                messagebox.showerror("Error", "Ya existe un usuario con ese nombre.")
                return

            # Insertar usuario administrador
            cursor.execute("""
                INSERT INTO usuario (nombre, contrasena, rol)
                VALUES (?, ?, 'admin')
            """, (nombre, contrasena))
            conexion.commit()
        except Exception as e:
            messagebox.showerror("Error al guardar", f"No se pudo crear el usuario:\n{e}")
            return
        finally:
            conexion.close()

        messagebox.showinfo("Éxito", f"Usuario administrador '{nombre}' creado correctamente.")
        entry_nombre.delete(0, tk.END)
        entry_contrasena.delete(0, tk.END)

    tk.Button(ventana, text="Registrar Usuario Admin", command=guardar, bg="lightblue").grid(
        row=3, column=0, columnspan=2, pady=20
    )

    if parent is None:
        ventana.mainloop()
