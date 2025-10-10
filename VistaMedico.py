import tkinter as tk
from tkinter import ttk, messagebox
from HistorialxPaciente import historialporpaciente
from TurnosAsignados import ventana_turnos_medico_logueado
from AgregarHistoriaClinica import agregar_historia_clinica  # <-- Importamos la función nueva

class VentanaMedico(tk.Toplevel):
    def __init__(self, maestro, usuario):
        super().__init__(maestro)
        self.maestro = maestro
        self.usuario = usuario
        self.title(f"Vista Médico - {usuario['nombre']}")
        self.resizable(False, False)

        # ===== Barra de menú =====
        barra = tk.Menu(self)
        self.config(menu=barra)
        menu_acciones = tk.Menu(barra, tearoff=0)
        menu_ayuda = tk.Menu(barra, tearoff=0)
        barra.add_cascade(label="Acciones", menu=menu_acciones)
        barra.add_cascade(label="Ayuda", menu=menu_ayuda)

        menu_acciones.add_command(label="Turnos Asignados", command=self.abrir_turnos_asignados)
        menu_acciones.add_command(label="Historial por Paciente", command=self.abrir_historial_por_paciente)
        menu_acciones.add_separator()
        menu_acciones.add_command(label="Cerrar sesión", command=self.cerrar_sesion)

        menu_ayuda.add_command(label="Acerca de…", command=self.acerca_de)

        # ===== Contenido principal =====
        cont = ttk.Frame(self, padding=12)
        cont.pack(fill="both", expand=True)

        ttk.Label(
            cont,
            text="Vista del Médico",
            font=("Segoe UI", 14, "bold")
        ).grid(row=0, column=0, columnspan=2, pady=(0, 10))

        botones = [
            ("Turnos Asignados", self.abrir_turnos_asignados),
            ("Historial por Paciente", self.abrir_historial_por_paciente),
            ("Agregar Historia Clínica", lambda: agregar_historia_clinica(self.usuario)),  # <-- NUEVO
            ("Cerrar sesión", self.cerrar_sesion),
        ]

        for i, (texto, cmd) in enumerate(botones, start=1):
            ttk.Button(cont, text=texto, command=cmd).grid(
                row=i, column=0, padx=8, pady=8, sticky="nsew"
            )

        cont.grid_columnconfigure(0, weight=1)

    # ===== Acciones =====
    def acerca_de(self):
        messagebox.showinfo("Acerca de", "Sistema de Turnos — Vista Médico")

    def abrir_turnos_asignados(self):
        """Abre la ventana de turnos (con selector de médicos)"""
        try:
            from TurnosAsignados import ventana_turnos_medico_logueado
            ventana_turnos_medico_logueado()  # No pasamos parámetros
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron mostrar los turnos asignados.\n\n{e}")


    def abrir_historial_por_paciente(self):
        """Abre la ventana de historial"""
        try:
            historialporpaciente()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir Historial.\n\n{e}")

    def cerrar_sesion(self):
        self.destroy()
        self.maestro.deiconify()
