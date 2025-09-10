import sqlite3
import tkinter as tk
from VistaAdmin import VentanaAdmin
from tkinter import messagebox

DB = "hospital.db"

def conectar_db():
    return sqlite3.connect(DB)

def registrar_usuario():
    nombre = entry_user.get().strip()
    contrasena = entry_pass.get().strip()
    rol = entry_rol.get().strip()

    if not nombre or not contrasena or not rol:
        messagebox.showwarning("Error", "Todos los campos son obligatorios")
        return

    conexion = conectar_db()
    cursor = conexion.cursor()
    try:
        cursor.execute("INSERT INTO usuario (nombre, contrasena, rol) VALUES (?, ?, ?)",
                       (nombre, contrasena, rol))
        conexion.commit()
        messagebox.showinfo("Éxito", "Usuario registrado correctamente")
        limpiar_campos()
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "El nombre de usuario ya existe")
    finally:
        conexion.close()

def limpiar_campos():
    entry_user.delete(0, tk.END)
    entry_pass.delete(0, tk.END)
    entry_rol.delete(0, tk.END)

def loguearse():
    nombre = entry_user.get().strip()
    contrasena = entry_pass.get().strip()

    if not nombre or not contrasena:
        messagebox.showwarning("Error", "Usuario y contraseña requeridos")
        return

    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT contrasena, rol FROM usuario WHERE nombre = ?", (nombre,))
    row = cursor.fetchone()
    conexion.close()

    if not row:
        messagebox.showerror("Error", "Usuario no encontrado")
    elif row[0] != contrasena:
        messagebox.showerror("Error", "Contraseña incorrecta")
    else:
        messagebox.showinfo("Bienvenido", f"Login correcto. Rol: {row[1]}")

        # Ocultar ventana actual (login)
        root.withdraw()

        # Abrir ventana de administración y guardar referencia para evitar que se cierre
        datos_usuario = {"nombre": nombre, "rol": row[1]}
        global ventana_admin
        ventana_admin = VentanaAdmin(root, datos_usuario)

        # Aquí se puede agregar lógica para cuando la ventana admin se cierre
        ventana_admin.protocol("WM_DELETE_WINDOW", on_cerrar_admin)

def on_cerrar_admin():
    # Cierra ventana admin, muestra login y limpia campos
    ventana_admin.destroy()
    limpiar_campos()
    root.deiconify()

# ---------------- Ventana Tkinter ----------------

root = tk.Tk()
root.title("Login / Registro")

tk.Label(root, text="Usuario").grid(row=0, column=0, padx=5, pady=5)
entry_user = tk.Entry(root)
entry_user.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Contraseña").grid(row=1, column=0, padx=5, pady=5)
entry_pass = tk.Entry(root, show="*")
entry_pass.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Rol").grid(row=2, column=0, padx=5, pady=5)
entry_rol = tk.Entry(root)
entry_rol.grid(row=2, column=1, padx=5, pady=5)

tk.Button(root, text="Ingresar", command=loguearse).grid(row=3, column=0, pady=10)
tk.Button(root, text="Registrar", command=registrar_usuario).grid(row=3, column=1, pady=10)

root.mainloop()
