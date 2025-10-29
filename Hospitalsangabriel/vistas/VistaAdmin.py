import tkinter as tk
from tkinter import messagebox, ttk

# --- Importaciones de funciones ---
from Hospitalsangabriel.Funcionesbd.VerTurno import ventana_turnos
from Hospitalsangabriel.Funcionesbd.AgregarMedico import agregarmedico
from Hospitalsangabriel.Funcionesbd.AgregarPaciente import agregar_paciente
from Hospitalsangabriel.Funcionesbd.AsignarTurno import asignarturno
from Hospitalsangabriel.Funcionesbd.HistorialxPaciente import historialporpaciente
from Hospitalsangabriel.Funcionesbd.ListarMedico import ventana_listar_medicos
from Hospitalsangabriel.Funcionesbd.ListarPaciente import ventana_listar_pacientes
from Hospitalsangabriel.Funcionesbd.Turnoxmedico import ventana_turnos_por_medico
from Hospitalsangabriel.Funcionesbd.AgregarUsuario import agregarusuario_admin  # ✅ corregido

class VentanaAdmin(tk.Toplevel):
    def __init__(self, maestro, usuario):
        super().__init__(maestro)
        self.maestro = maestro
        self.usuario = usuario

        self.title(f"Panel de Administración - {usuario['nombre']}")
        self.geometry("600x400")
        self.resizable(False, False)

        # ===== Barra de menú =====
        barra = tk.Menu(self)
        self.config(menu=barra)
        menu_acciones = tk.Menu(barra, tearoff=0)
        menu_ayuda = tk.Menu(barra, tearoff=0)
        barra.add_cascade(label="Acciones", menu=menu_acciones)
        barra.add_cascade(label="Ayuda", menu=menu_ayuda)

        # ===== Contenedor principal =====
        cont = ttk.Frame(self, padding=12)
        cont.pack(fill="both", expand=True)

        ttk.Label(cont, text="Panel de Administración", font=("Segoe UI", 14, "bold")).grid(
            row=0, column=0, columnspan=3, pady=(0, 10)
        )

        # ===== Lista de botones =====
        botones_info = [
            ("Agregar Médico", self.abrir_agregar_medico),
            ("Agregar Paciente", self.abrir_agregar_paciente),
            ("Agregar Usuario", self.abrir_agregar_usuario),
            ("Asignar Turno", self.abrir_asignar_turno),
            ("Historial por Paciente", self.abrir_historial_por_paciente),
            ("Listar Médicos", self.abrir_listar_medicos),
            ("Listar Pacientes", self.abrir_listarpacientes),
            ("Turnos por Médico", self.abrir_turnos_por_medico),
            ("Ver Turno", self.abrir_ver_turno),
            ("Cerrar sesión", self.cerrar_sesion)
        ]

        fila, col = 1, 0
        for texto, cmd in botones_info:
            btn = ttk.Button(cont, text=texto, command=cmd)
            btn.grid(row=fila, column=col, padx=8, pady=8, sticky="nsew")
            col += 1
            if col == 3:
                col = 0
                fila += 1

        # ===== Menú Acciones =====
        menu_acciones.add_command(label="Agregar Médico", command=self.abrir_agregar_medico)
        menu_acciones.add_command(label="Agregar Paciente", command=self.abrir_agregar_paciente)
        menu_acciones.add_command(label="Agregar Usuario", command=self.abrir_agregar_usuario)
        menu_acciones.add_separator()
        menu_acciones.add_command(label="Cerrar sesión", command=self.cerrar_sesion)

        # ===== Menú Ayuda =====
        menu_ayuda.add_command(label="Acerca de…", command=self.acerca_de)

    # ===== Métodos de acciones =====
    def acerca_de(self):
        messagebox.showinfo("Acerca de", "Sistema de Turnos — Panel Admin")

    def abrir_agregar_medico(self):
        try:
            agregarmedico(parent=self)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir la ventana de médicos:\n{e}")

    def abrir_agregar_paciente(self):
        try:
            agregar_paciente(parent=self)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir la ventana de pacientes:\n{e}")

    def abrir_agregar_usuario(self):
        try:
            agregarusuario_admin(parent=self)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir la ventana de usuarios:\n{e}")

    def abrir_asignar_turno(self):
        try:
            asignarturno(parent=self)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir la ventana de turnos:\n{e}")

    def abrir_historial_por_paciente(self):
        try:
            historialporpaciente(parent=self)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el historial:\n{e}")

    def abrir_listar_medicos(self):
        try:
            ventana_listar_medicos(parent=self)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir la lista de médicos:\n{e}")

    def abrir_listarpacientes(self):
        try:
            ventana_listar_pacientes(parent=self)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir la lista de pacientes:\n{e}")

    def abrir_turnos_por_medico(self):
        try:
            ventana_turnos_por_medico(parent=self)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir la vista de turnos por médico:\n{e}")

    def abrir_ver_turno(self):
        try:
            ventana_turnos(parent=self)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir la vista de turnos:\n{e}")

    def cerrar_sesion(self):
        self.destroy()
        self.maestro.deiconify()
