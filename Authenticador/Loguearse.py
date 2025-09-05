import sqlite3
import tkinter as tk
from tkinter import messagebox

# Auth vive en el mismo paquete Authenticador
from .autenticador import Auth   # <- relativo

DB = "hospital.db"

def registrar_usuario():
    nombre = entry_user.get().strip()
    contrasena = entry_pass.get().strip()
    rol = entry_rol.get().strip()

    if not nombre or not contrasena or not rol:
        messagebox.showwarning("Error", "Todos los campos son obligatorios")
        return

    con = sqlite3.connect(DB)
    cur = con.cursor()
    try:
        cur.execute("INSERT INTO usuario (nombre, contrasena, rol) VALUES (?, ?, ?)",
                    (nombre, contrasena, rol))
        con.commit()
        messagebox.showinfo("Éxito", "Usuario registrado correctamente")
        entry_user.delete(0, tk.END)
        entry_pass.delete(0, tk.END)
        entry_rol.delete(0, tk.END)
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "El nombre de usuario ya existe")
    finally:
        con.close()

def autenticar_usuario(nombre, contrasena):
    # Primero intento con tu Auth
    try:
        datos = Auth.autenticar(nombre, contrasena)
        if datos:
            return datos
    except AttributeError:
        pass

    # Fallback local
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("SELECT id, nombre, contrasena, rol FROM usuario WHERE nombre=? LIMIT 1", (nombre,))
    fila = cur.fetchone()
    con.close()
    if not fila or fila[2] != contrasena:
        return None
    return {"id": fila[0], "nombre": fila[1], "rol": fila[3]}

def loguearse():
    nombre = entry_user.get().strip()
    contrasena = entry_pass.get().strip()

    if not nombre or not contrasena:
        messagebox.showwarning("Error", "Usuario y contraseña requeridos")
        return

    usuario = autenticar_usuario(nombre, contrasena)
    if not usuario:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")
        return

    if str(usuario["rol"]).lower() != "admin":
        messagebox.showinfo("Acceso", "No sos admin. Acceso limitado.")
        return

    # IMPORTANTÍSIMO: import tardío para evitar el ciclo
    from .VistaAdmin import VentanaAdmin

    root.withdraw()
    VentanaAdmin(root, usuario)

# ---------------- UI Login ----------------
root = tk.Tk()
root.title("Login / Registro")

tk.Label(root, text="Usuario").grid(row=0, column=0, padx=5, pady=5)
entry_user = tk.Entry(root); entry_user.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Contraseña").grid(row=1, column=0, padx=5, pady=5)
entry_pass = tk.Entry(root, show="*"); entry_pass.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Rol").grid(row=2, column=0, padx=5, pady=5)
entry_rol = tk.Entry(root); entry_rol.grid(row=2, column=1, padx=5, pady=5)

tk.Button(root, text="Ingresar", command=loguearse).grid(row=3, column=0, pady=10, sticky="we")
tk.Button(root, text="Registrar", command=registrar_usuario).grid(row=3, column=1, pady=10, sticky="we")

if __name__ == "__main__":
    root.mainloop()
