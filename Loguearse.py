import sqlite3
import tkinter as tk
from VistaAdmin import VentanaAdmin
from tkinter import messagebox

DB = "hospital.db"

def conectar_db():
    return sqlite3.connect(DB)

def loguearse():
    nombre = entry_user.get().strip()
    contrasena = entry_pass.get().strip()
    
    if not nombre or not contrasena:
        messagebox.showwarning("Error", "Usuario y contraseña requeridos")
        return

    conexion = conectar_db()
    cursor = conexion.cursor()

    cursor.execute("SELECT id, contrasena, rol, persona_id FROM usuario WHERE nombre = ?", (nombre,))
    row = cursor.fetchone()
    conexion.close()

    if not row:
        messagebox.showerror("Error", "Usuario no encontrado")
    elif row[1] != contrasena:
        messagebox.showerror("Error", "Contraseña incorrecta")
    else:
        usuario_id, _, rol, persona_id = row
        if rol not in ("admin", "recepcionista"):
            messagebox.showwarning("Acceso denegado", "Solo administradores y recepcionistas pueden acceder a esta vista.")
            return
        messagebox.showinfo("Bienvenido", f"Login correcto. Rol: {rol}")
        root.withdraw()

        datos_usuario = {
            "id": usuario_id,
            "nombre": nombre,
            "rol": rol,
            "persona_id": persona_id
        }
        global ventana_admin
        ventana_admin = VentanaAdmin(root, datos_usuario)
        ventana_admin.protocol("WM_DELETE_WINDOW", on_cerrar_admin)

def on_cerrar_admin():
    ventana_admin.destroy()
    root.deiconify()

def limpiar_datos():
    entry_user.delete(0, tk.END)
    entry_pass.delete(0, tk.END)

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
