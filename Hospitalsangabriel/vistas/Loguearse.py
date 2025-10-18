import sqlite3
import tkinter as tk
from vistas.VistaAdmin import VentanaAdmin
from vistas.VistaMedico import VentanaMedico
from tkinter import messagebox

DB = "hospital.db"

def conectar_db():
    return sqlite3.connect(DB)

def on_cerrar_admin():
    ventana_admin.destroy()
    root.deiconify()

def limpiar_datos():
    entry_user.delete(0, tk.END)
    entry_pass.delete(0, tk.END)

def loguearse():
    nombre = entry_user.get().strip()
    contrasena = entry_pass.get().strip()
    
    if not nombre or not contrasena:
        messagebox.showwarning("Error", "Usuario y contraseña requeridos")
        return

    try:
        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute("SELECT id, contrasena, rol FROM usuario WHERE nombre = ?", (nombre,))
        row = cursor.fetchone()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo conectar a la base de datos:\n{e}")
        return
    finally:
        conexion.close()

    if not row:
        messagebox.showerror("Error", "Usuario no encontrado")
        return

    usuario_id, password_db, rol = row
    rol = rol.strip().lower()

    if contrasena != password_db:
        messagebox.showerror("Error", "Contraseña incorrecta")
        return

    # --- Enrutamiento por rol ---
    root.withdraw()
    datos_usuario = {"id": usuario_id, "nombre": nombre, "rol": rol}

    if rol in ("admin", "recepcionista"):
        messagebox.showinfo("Bienvenido", f"Login correcto. Rol: {rol}")
        global ventana_admin
        ventana_admin = VentanaAdmin(root, datos_usuario)
        ventana_admin.protocol("WM_DELETE_WINDOW", on_cerrar_admin)

    elif rol == "medico":
        messagebox.showinfo("Bienvenido", "Login correcto. Rol: médico")
        # Abrir la vista de médico
        ventana = VentanaMedico(root,datos_usuario)
        def on_cerrar_medico():
            ventana.destroy()
            root.deiconify()
        ventana.protocol("WM_DELETE_WINDOW", on_cerrar_medico)

    else:
        messagebox.showwarning("Acceso denegado", "Tu usuario no tiene permisos para acceder.")
        root.deiconify()


# --- Interfaz ---
root = tk.Tk()
root.title("Iniciar sesión")
root.geometry("300x180")  # Ajusta el tamaño de la ventana

# Etiqueta y campo para usuario
label_user = tk.Label(root, text="Nombre:")
label_user.pack(pady=(20, 0))
entry_user = tk.Entry(root)
entry_user.pack()

# Etiqueta y campo para contraseña
label_pass = tk.Label(root, text="Contraseña:")
label_pass.pack(pady=(10, 0))
entry_pass = tk.Entry(root, show="*")
entry_pass.pack()

# Botón de login
btn_login = tk.Button(root, text="Iniciar sesión", command=loguearse)
btn_login.pack(pady=(15, 5))

# Botón de limpiar datos
btn_limpiar = tk.Button(root, text="Limpiar datos", command=limpiar_datos)
btn_limpiar.pack()


root.mainloop()
