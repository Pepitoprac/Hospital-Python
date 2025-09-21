import tkinter as tk
from tkinter import messagebox, ttk

from VerTurno import verturno
from AgregarMedico import agregarmedico
from AgregarPaciente import agregar_paciente
from AsignarTurno import asignarturno
from AtenderProximo import atenderproximo
from HistorialxPaciente import historialporpaciente
from ListarMedico import ventana_listar_medicos
from ListarPaciente import ventana_listar_pacientes
from Turnoxmedico import ventana_turnos_por_medico


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

        # Botones asociados a métodos
        botones_info = [
            ("Agregar Médico", self.abrir_agregar_medico),
            ("Agregar Paciente", self.abrir_agregar_paciente),
            ("Asignar Turno (UI)", self.abrir_asignar_turno),
            ("Atender Próximo", self.abrir_atender_proximo),
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

        # Menú Acciones
        menu_acciones.add_command(label="Agregar Médico", command=self.abrir_agregar_medico)
        menu_acciones.add_command(label="Agregar Paciente", command=self.abrir_agregar_paciente)
        menu_acciones.add_command(label="Asignar Turno (UI)", command=self.abrir_asignar_turno)
        menu_acciones.add_separator()
        menu_acciones.add_command(label="Cerrar sesión", command=self.cerrar_sesion)

        # Menú Ayuda
        menu_ayuda.add_command(label="Acerca de…", command=self.acerca_de)

    def acerca_de(self):
        messagebox.showinfo("Acerca de", "Sistema de Turnos — Panel Admin")

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
            # ✅ Le pasamos el ID del usuario (médico)
            atenderproximo(self.usuario["id"])
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def abrir_historial_por_paciente(self):
        try:
            historialporpaciente()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def abrir_listar_medicos(self):
        try:
            ventana_listar_medicos()
        except Exception as e:
            messagebox.showerror("Error", str(e))


    def abrir_listarpacientes(self):
        try:
            ventana_listar_pacientes()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def abrir_turnos_por_medico(self):
        try:
            ventana_turnos_por_medico()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def abrir_ver_turno(self):
        def consultar():
            try:
                id_turno = int(entrada_id.get())
                datos = verturno(id_turno)
                if datos:
                    mensaje = (
                        f"ID Turno: {datos[0]}\n"
                        f"Paciente: {datos[1]}\n"
                        f"Médico: {datos[2]}\n"
                        f"Fecha: {datos[3]}\n"
                        f"Hora: {datos[4]}\n"
                        f"Urgencia: {'Sí' if datos[5] else 'No'}\n"
                        f"Área: {datos[6]}"
                    )
                    messagebox.showinfo("Datos del Turno", mensaje)
                else:
                    messagebox.showwarning("Sin resultados", f"No se encontró el turno con ID {id_turno}")
                ventana.destroy()
            except ValueError:
                messagebox.showerror("Error", "Por favor ingrese un ID válido (número entero).")
                ventana.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))
                ventana.destroy()

        # Crear ventana emergente
        ventana = tk.Toplevel(self)
        ventana.title("Ver Turno")
        ventana.resizable(False, False)
        ventana.grab_set()

        ttk.Label(ventana, text="Ingrese ID del Turno:").pack(padx=10, pady=(10, 5))
        entrada_id = ttk.Entry(ventana)
        entrada_id.pack(padx=10, pady=5)
        ttk.Button(ventana, text="Consultar", command=consultar).pack(pady=(5, 10))

    def cerrar_sesion(self):
        self.destroy()
        self.maestro.deiconify()
