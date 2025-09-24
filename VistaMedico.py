import tkinter as tk
from tkinter import ttk, messagebox
from HistorialxPaciente import historialporpaciente 
from VerTurno import ver_turnos
from VerTurno import ventana_turnos_medico

"""en historial paciente tendria que haber 2 botones uno para vizualizarlo y el otro para actualizarlo y que le haga un update"""
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

        menu_acciones.add_command(label="Ver Turnos", command=self.abrir_ver_turno)
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
            ("Ver Turnos", self.abrir_ver_turno),
            ("Historial por Paciente", self.abrir_historial_por_paciente),
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

    def abrir_ver_turno(self):
        try:
            ver_turnos(self)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def abrir_historial_por_paciente(self):
        try:
            historialporpaciente()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir Historial.\n\n{e}")

    def cerrar_sesion(self):
        self.destroy()
        self.maestro.deiconify()

        # dentro de VentanaMedico
    def abrir_ver_turno(self):
        ventana_turnos_medico(self, medico_id=self.usuario["id"], solo_hoy=False)  # o True para solo hoy


    

    
