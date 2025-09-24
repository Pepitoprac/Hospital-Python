import tkinter as tk
from tkinter import messagebox, ttk

from HistorialxPaciente import historialporpaciente

import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

# Reutilizamos el mismo nombre de DB que el resto del proyecto
DB = "hospital.db"

# Historial por paciente (si existe en el proyecto)
try:
    from HistorialxPaciente import historialporpaciente
except Exception:
    historialporpaciente = None

def conectar_db():
    return sqlite3.connect(DB)

def obtener_medicos():
    """Devuelve [(id, nombre)] de la tabla medico."""
    con = conectar_db()
    cur = con.cursor()
    cur.execute("SELECT id, nombre FROM medico ORDER BY nombre;")
    datos = cur.fetchall()
    con.close()
    return datos

def obtener_turnos_por_medico_y_fecha(medico_id, fecha_yyyy_mm_dd):
    """
    Devuelve lista de turnos:
    (id, paciente, fecha, hora, urgencia, paciente_id)
    filtrado por medico_id y fecha (YYYY-MM-DD).
    """
    con = conectar_db()
    cur = con.cursor()
    cur.execute("""
        SELECT 
            t.id,
            p.nombre AS paciente,
            t.fecha,
            t.hora,
            t.urgencia,
            p.id as paciente_id
        FROM turno t
        JOIN paciente p ON t.paciente_id = p.id
        WHERE t.medico_id = ? AND t.fecha = ?
        ORDER BY t.hora ASC;
    """, (medico_id, fecha_yyyy_mm_dd))
    filas = cur.fetchall()
    con.close()
    return filas

class VistaMedico(tk.Toplevel):
    """
    Ventana para que el MÉDICO vea sus turnos del día, con filtro por fecha.
    Compatible con el esquema típico del proyecto (Tkinter + SQLite).
    """
    def __init__(self, maestro=None, *, medico_id=None):
        super().__init__(master=maestro)
        self.title("Vista Médico")
        self.geometry("820x520")
        self.resizable(True, True)

        # Estado interno
        self._medicos = []       # [(id, nombre), ...]
        self._medico_sel = None  # (id, nombre)
        self._turno_sel = None   # turno_id
        self._paciente_sel = None  # paciente_id

        # Header
        top = ttk.Frame(self, padding=10)
        top.pack(fill="x")

        ttk.Label(top, text="Médico:", width=8).grid(row=0, column=0, sticky="w")
        self.cbo_medico = ttk.Combobox(top, state="readonly", width=35)
        self.cbo_medico.grid(row=0, column=1, sticky="w")
        self.cbo_medico.bind("<<ComboboxSelected>>", lambda e: self.cargar_turnos())

        ttk.Label(top, text="Fecha (YYYY-MM-DD):", width=22).grid(row=0, column=2, sticky="e", padx=(10, 4))
        self.ent_fecha = ttk.Entry(top, width=14)
        self.ent_fecha.grid(row=0, column=3, sticky="w")
        self.ent_fecha.insert(0, date.today().strftime("%Y-%m-%d"))

        ttk.Button(top, text="Hoy", command=self._set_hoy).grid(row=0, column=4, padx=4)
        ttk.Button(top, text="Cargar", command=self.cargar_turnos).grid(row=0, column=5, padx=4)

        # Tabla turnos
        mid = ttk.Frame(self, padding=(10, 0, 10, 10))
        mid.pack(fill="both", expand=True)

        cols = ("Hora", "Paciente", "Urgencia", "Fecha", "turno_id", "paciente_id")
        self.tabla = ttk.Treeview(mid, columns=cols, show="headings", height=16)
        self.tabla.heading("Hora", text="Hora")
        self.tabla.heading("Paciente", text="Paciente")
        self.tabla.heading("Urgencia", text="Urgencia")
        self.tabla.heading("Fecha", text="Fecha")
        # IDs ocultas
        self.tabla.heading("turno_id", text="turno_id")
        self.tabla.heading("paciente_id", text="paciente_id")

        self.tabla.column("Hora", width=90, anchor="center")
        self.tabla.column("Paciente", width=280, anchor="w")
        self.tabla.column("Urgencia", width=120, anchor="center")
        self.tabla.column("Fecha", width=110, anchor="center")
        self.tabla.column("turno_id", width=0, stretch=False)
        self.tabla.column("paciente_id", width=0, stretch=False)

        vsb = ttk.Scrollbar(mid, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscroll=vsb.set)
        self.tabla.pack(side="left", fill="both", expand=True)
        vsb.pack(side="left", fill="y")

        self.tabla.bind("<<TreeviewSelect>>", self._on_select)
        self.tabla.bind("<Double-1>", self._on_double_click)

        # Panel inferior (acciones / estado)
        bottom = ttk.Frame(self, padding=(10, 8, 10, 10))
        bottom.pack(fill="x")

        self.lbl_paciente = ttk.Label(bottom, text="Paciente: -", font=("Segoe UI", 11, "bold"))
        self.lbl_paciente.grid(row=0, column=0, sticky="w")

        self.btn_historial = ttk.Button(
            bottom, text="Ver historial del paciente", command=self._ver_historial, state="disabled"
        )
        self.btn_historial.grid(row=0, column=1, sticky="e", padx=(10, 0))

        # Status bar
        self.status = tk.StringVar(value="Listo")
        barra = ttk.Label(self, textvariable=self.status, relief="sunken", anchor="w")
        barra.pack(side="bottom", fill="x")

        # Cargar datos iniciales
        self._cargar_medicos()
        if medico_id is not None:
            self._seleccionar_medico_por_id(medico_id)
        else:
            if self._medicos:
                self.cbo_medico.current(0)
        self.cargar_turnos()

    # --------- Helpers UI
    def _set_status(self, msg):
        self.status.set(msg)
        self.after(4000, lambda: self.status.set("Listo"))

    def _set_hoy(self):
        self.ent_fecha.delete(0, "end")
        self.ent_fecha.insert(0, date.today().strftime("%Y-%m-%d"))

    def _cargar_medicos(self):
        try:
            self._medicos = obtener_medicos()
            self.cbo_medico["values"] = [m[1] for m in self._medicos]
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los médicos.\n\n{e}")

    def _seleccionar_medico_por_id(self, medico_id):
        for i, (mid, _) in enumerate(self._medicos):
            if int(mid) == int(medico_id):
                self.cbo_medico.current(i)
                return

    # --------- Carga turnos
    def cargar_turnos(self):
        if not self._medicos or self.cbo_medico.current() < 0:
            self._limpiar_tabla()
            return
        idx = self.cbo_medico.current()
        med_id, med_nom = self._medicos[idx]
        fecha = self.ent_fecha.get().strip() or date.today().strftime("%Y-%m-%d")

        try:
            filas = obtener_turnos_por_medico_y_fecha(med_id, fecha)
            self._limpiar_tabla()
            for t_id, pac, fec, hor, urg, pac_id in filas:
                self.tabla.insert("", "end", values=(hor or "", pac or "", urg or "", fec or "", t_id, pac_id))
            self._medico_sel = (med_id, med_nom)
            self._turno_sel = None
            self._paciente_sel = None
            self.lbl_paciente.config(text="Paciente: -")
            self.btn_historial.config(state="disabled")
            self._set_status(f"Turnos cargados: {len(filas)} — {med_nom} — {fecha}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los turnos.\n\n{e}")

    def _limpiar_tabla(self):
        for it in self.tabla.get_children():
            self.tabla.delete(it)

    # --------- Eventos
    def _on_select(self, event=None):
        sel = self.tabla.selection()
        if not sel:
            return
        vals = self.tabla.item(sel[0], "values")
        self._turno_sel = int(vals[4]) if vals[4] else None
        self._paciente_sel = int(vals[5]) if vals[5] else None
        self.lbl_paciente.config(text=f"Paciente: {vals[1]}")
        self.btn_historial.config(state="normal" if self._paciente_sel and historialporpaciente else "disabled")

    def _on_double_click(self, event=None):
        # Doble clic -> historial si está disponible
        if self._paciente_sel and historialporpaciente:
            self._ver_historial()

    def _ver_historial(self):
        if not self._paciente_sel:
            messagebox.showinfo("Atención", "Seleccioná un turno/paciente.")
            return
        if historialporpaciente is None:
            messagebox.showwarning("Info", "El módulo de historial no está disponible.")
            return
        try:
            # Algunas versiones de historialporpaciente no reciben parámetros;
            # si tu función requiere paciente_id, adaptá aquí.
            try:
                historialporpaciente(self._paciente_sel)  # intento con parámetro
            except TypeError:
                historialporpaciente()  # fallback sin parámetro
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el historial.\n\n{e}")
    
    

def ventana_medico(parent=None, medico_id=None):
    """
    Helper para abrir como sub-ventana (similar a la organización de tus vistas).
    """
    win = VistaMedico(parent, medico_id=medico_id)
    win.transient(parent)
    win.grab_set()
    return win

# Permite ejecutar esta vista en forma independiente (para pruebas)
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Launcher — Vista Médico")
    tk.Label(root, text="Abrir Vista Médico").pack(padx=10, pady=(10, 0))
    tk.Button(root, text="Abrir", command=lambda: VistaMedico(root)).pack(pady=10)
    root.mainloop()

