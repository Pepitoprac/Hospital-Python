import tkinter as tk
from tkinter import messagebox, ttk

# NO importes Loguearse ni Auth acá (evita el ciclo)

# Importá las funciones desde el paquete hermano Funcionesbd (relativos)
import os, sys
if __package__ is None or __package__ == "":
    # agregado al sys.path la carpeta padre de Authenticador (que contiene Funcionesbd)
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    from Funcionesbd.AgregarMedico import agregarmedico
    from Funcionesbd.AgregarPaciente import agregar_paciente
    from Funcionesbd.AsignarTurno import asignarturno
    from Funcionesbd.AtenderProximo import atenderproximo
    from Funcionesbd.HistorialxPaciente import historialporpaciente
    from Funcionesbd.ListarHistorialxPaciente import listar_historial_pacientes
    from Funcionesbd.ListarMedico import listarmedico
    from Funcionesbd.ListarPaciente import listarpaciente
    from Funcionesbd.Turnoxmedico import verturnopormedico
    from Funcionesbd.VerHistorial import verhistorial
    from Funcionesbd.VerTurno import verturno
else:
    # camino normal (paquete)
    from ..Funcionesbd.AgregarMedico import agregarmedico
    from ..Funcionesbd.AgregarPaciente import agregar_paciente
    from ..Funcionesbd.AsignarTurno import asignarturno
    from ..Funcionesbd.AtenderProximo import atenderproximo
    from ..Funcionesbd.HistorialxPaciente import historialporpaciente
    from ..Funcionesbd.ListarHistorialxPaciente import listar_historial_pacientes
    from ..Funcionesbd.ListarMedico import listarmedico
    from ..Funcionesbd.ListarPaciente import listarpaciente
    from ..Funcionesbd.Turnoxmedico import verturnopormedico
    from ..Funcionesbd.VerHistorial import verhistorial
    from ..Funcionesbd.VerTurno import verturno

class VentanaAdmin(tk.Toplevel):
    def __init__(self, maestro, usuario):
        tk.Toplevel.__init__(self, maestro)
        self.maestro = maestro
        self.usuario = usuario
        self.title(f"Panel de Administración - {usuario['nombre']}")
        self.resizable(False, False)

        barra = tk.Menu(self)
        self.config(menu=barra)
        menu_acciones = tk.Menu(barra, tearoff=0)
        menu_ayuda = tk.Menu(barra, tearoff=0)
        barra.add_cascade(label="Acciones", menu=menu_acciones)
        barra.add_cascade(label="Ayuda", menu=menu_ayuda)

        cont = ttk.Frame(self, padding=12)
        cont.pack(fill="both", expand=True)

        ttk.Label(cont, text="Panel de Administración", font=("Segoe UI", 14, "bold")).grid(
            row=0, column=0, columnspan=3, pady=(0, 10)
        )

        b1 = ttk.Button(cont, text="Agregar Médico", command=agregarmedico)
        b2 = ttk.Button(cont, text="Agregar Paciente", command=agregar_paciente)
        b3 = ttk.Button(cont, text="Asignar Turno (UI)", command=asignarturno)
        b4 = ttk.Button(cont, text="Atender Próximo", command=atender_proximo)
        b5 = ttk.Button(cont, text="Historial por Paciente", command=historialporpaciente)
        b6 = ttk.Button(cont, text="Listar Historial Pacientes", command=listar_historial_pacientes)
        b7 = ttk.Button(cont, text="Listar Médicos", command=listarmedico)
        b8 = ttk.Button(cont, text="Listar Pacientes", command=listarpaciente)
        b9 = ttk.Button(cont, text="Turnos por Médico", command=verturnopormedico)
        b10 = ttk.Button(cont, text="Ver Historial", command=verhistorial)
        b11 = ttk.Button(cont, text="Ver Turno", command=verturno)
        b12 = ttk.Button(cont, text="Cerrar sesión", command=self.cerrar_sesion)

        botones = [b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11,b12]
        fila, col = 1, 0
        for btn in botones:
            btn.grid(row=fila, column=col, padx=8, pady=8, sticky="nsew")
            col += 1
            if col == 3:
                col = 0
                fila += 1

        # (Opcional) Bloque "Asignar turno rápido" si querés
        # podés reusar lo que ya te dejé antes

        # Menú
        menu_acciones.add_command(label="Agregar Médico", command=self.abrir_agregar_medico)
        menu_acciones.add_command(label="Agregar Paciente", command=self.abrir_agregar_paciente)
        menu_acciones.add_command(label="Asignar Turno (UI)", command=self.abrir_asignar_turno)
        menu_acciones.add_separator()
        menu_acciones.add_command(label="Cerrar sesión", command=self.cerrar_sesion)

        def acerca_de():
            messagebox.showinfo("Acerca de", "Sistema de Turnos — Panel Admin")
        menu_ayuda.add_command(label="Acerca de…", command=acerca_de)

    # --- Abridores (sin lambda) ---
    def abrir_agregar_medico(self):
        try: agregarmedico()
        except Exception as e: messagebox.showerror("Error", str(e))

    def abrir_agregar_paciente(self):
        try: agregar_paciente()
        except Exception as e: messagebox.showerror("Error", str(e))

    def abrir_asignar_turno(self):
        try: asignarturno()
        except Exception as e: messagebox.showerror("Error", str(e))

    def abrir_atender_proximo(self):
        try: atender_proximo()
        except Exception as e: messagebox.showerror("Error", str(e))

    def abrir_historial_por_paciente(self):
        try: historialporpaciente()
        except Exception as e: messagebox.showerror("Error", str(e))

    def abrir_listar_historial_pacientes(self):
        try: listar_historial_pacientes()
        except Exception as e: messagebox.showerror("Error", str(e))

    def abrir_listar_medicos(self):
        try: listarmedico()
        except Exception as e: messagebox.showerror("Error", str(e))

    def abrir_listarpacientes(self):
        try: listarpaciente()
        except Exception as e: messagebox.showerror("Error", str(e))

    def abrir_turnos_por_medico(self):
        try: verturnopormedico()
        except Exception as e: messagebox.showerror("Error", str(e))

    def abrir_ver_historial(self):
        try: verhistorial()
        except Exception as e: messagebox.showerror("Error", str(e))

    def abrir_ver_turno(self):
        try: verturno()
        except Exception as e: messagebox.showerror("Error", str(e))

    def cerrar_sesion(self):
        self.destroy()
        self.maestro.deiconify()
