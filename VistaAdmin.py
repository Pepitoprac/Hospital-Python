import tkinter as tk
from tkinter import messagebox, ttk

from AgregarMedico import agregarmedico
from AgregarPaciente import agregar_paciente
from AsignarTurno import asignarturno
from AtenderProximo import atenderproximo
from HistorialxPaciente import historialporpaciente
from ListarHistorialxPaciente import listar_historial_pacientes
from ListarMedico import listarmedico
from ListarPaciente import listarpaciente
from Turnoxmedico import verturnopormedico
from VerHistorial import verhistorial
from VerTurno import verturno


class VentanaAdmin(tk.Toplevel):
    def __init__(self, maestro, usuario):
        super().__init__(maestro)
        self.maestro = maestro
        self.usuario = usuario
        self.title(f"Panel de Administración - {usuario['nombre']}")
        self.resizable(False, False)

        # Crear barra de menú
        barra = tk.Menu(self)
        self.config(menu=barra)
        menu_acciones = tk.Menu(barra, tearoff=0)
        menu_ayuda = tk.Menu(barra, tearoff=0)
        barra.add_cascade(label="Acciones", menu=menu_acciones)
        barra.add_cascade(label="Ayuda", menu=menu_ayuda)

        # Frame principal
        cont = ttk.Frame(self, padding=12)
        cont.pack(fill="both", expand=True)

        ttk.Label(cont, text="Panel de Administración", font=("Segoe UI", 14, "bold")).grid(
            row=0, column=0, columnspan=3, pady=(0, 10)
        )

        # Botones asociados a métodos que manejan excepciones
        botones_info = [
            ("Agregar Médico", self.abrir_agregar_medico),
            ("Agregar Paciente", self.abrir_agregar_paciente),
            ("Asignar Turno (UI)", self.abrir_asignar_turno),
            ("Atender Próximo", self.abrir_atender_proximo),
            ("Historial por Paciente", self.abrir_historial_por_paciente),
            ("Listar Historial Pacientes", self.abrir_listar_historial_pacientes),
            ("Listar Médicos", self.abrir_listar_medicos),
            ("Listar Pacientes", self.abrir_listarpacientes),
            ("Turnos por Médico", self.abrir_turnos_por_medico),
            ("Ver Historial", self.abrir_ver_historial),
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

        # Menú Acciones con las mismas funciones que botones
        menu_acciones.add_command(label="Agregar Médico", command=self.abrir_agregar_medico)
        menu_acciones.add_command(label="Agregar Paciente", command=self.abrir_agregar_paciente)
        menu_acciones.add_command(label="Asignar Turno (UI)", command=self.abrir_asignar_turno)
        menu_acciones.add_separator()
        menu_acciones.add_command(label="Cerrar sesión", command=self.cerrar_sesion)

        # Menú Ayuda
        menu_ayuda.add_command(label="Acerca de…", command=self.acerca_de)

    def acerca_de(self):
        messagebox.showinfo("Acerca de", "Sistema de Turnos — Panel Admin")

    # Métodos para abrir ventanas con manejo de excepciones
    def abrir_agregar_medico(self):
        try:
            agregarmedico()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def abrir_agregar_paciente(self):
        try:
            agregar_paciente()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def abrir_asignar_turno(self):
        try:
            asignarturno()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def abrir_atender_proximo(self):
        try:
            atenderproximo()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def abrir_historial_por_paciente(self):
        try:
            historialporpaciente()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def abrir_listar_historial_pacientes(self):
        try:
            listar_historial_pacientes()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def abrir_listar_medicos(self):
        try:
            listarmedico()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def abrir_listarpacientes(self):
        try:
            listarpaciente()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def abrir_turnos_por_medico(self):
        try:
            verturnopormedico()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def abrir_ver_historial(self):
        try:
            verhistorial()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def abrir_ver_turno(self):
        try:
            verturno()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def cerrar_sesion(self):
        self.destroy()
        self.maestro.deiconify()
