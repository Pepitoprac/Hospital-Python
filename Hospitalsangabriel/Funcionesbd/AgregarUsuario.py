import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from rutadb import DB as RutaDb

DB_PATH = RutaDb

def agregar_usuario(parent=None):
    ventana = tk.Toplevel(parent) if parent else tk.Tk()
    ventana.title("Agregar Usuario")
    ventana.geometry("300x200")

    # --- Campos ---
    tk.Label(ventana, text="Nombre:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    entry_nombre = tk.Entry(ventana)
    entry_nombre.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(ventana, text="Contraseña:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    entry_clave = tk.Entry(ventana, show="*")
    entry_clave.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(ventana, text="Rol:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    combo_rol = ttk.Combobox(ventana, state="readonly", values=["admin", "medico", "recepcionista"])
    combo_rol.grid(row=2, column=1, padx=10, pady=5)
    combo_rol.set("Seleccionar rol")

    # --- Función guardar ---
    def guardar():
        nombre = entry_nombre.get().strip()
        clave = entry_clave.get().strip()
        rol = combo_rol.get().strip()

        if not nombre or not clave or rol == "Seleccionar rol":
            messagebox.showwarning("Error", "Todos los campos son obligatorios")
            return

        try:
            conexion = sqlite3.connect(DB_PATH)
            cursor = conexion.cursor()
            cursor.execute(
                "INSERT INTO usuario (nombre, contrasena, rol) VALUES (?, ?, ?)",
                (nombre, clave, rol)
            )
            conexion.commit()
        except sqlite3.IntegrityError as e:
            messagebox.showerror("Error", f"Error de integridad:\n{e}")
            return
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el usuario:\n{e}")
            return
        finally:
            try: conexion.close()
            except: pass

        messagebox.showinfo("Éxito", f"Usuario '{nombre}' creado correctamente")
        entry_nombre.delete(0, tk.END)
        entry_clave.delete(0, tk.END)
        combo_rol.set("Seleccionar rol")

    # --- Botón ---
    tk.Button(ventana, text="Guardar Usuario", command=guardar, bg="lightgreen").grid(
        row=3, column=0, columnspan=2, pady=15
    )

    # Si se ejecuta standalone, iniciar mainloop
    if parent is None:
        ventana.mainloop()


