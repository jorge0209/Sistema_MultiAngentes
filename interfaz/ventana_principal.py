import tkinter as tk
from datetime import datetime
from tkinter import ttk, messagebox

from modelo.organizacion import SistemaMultiAgenteInundaciones
from modelo.entorno import CiudadCartagena
from modelo.reporte import CATEGORIAS, BARRIOS

COLORES = {"Bajo": "#2e8b57", "Medio": "#d4a017", "Alto": "#e67e22", "Crítico": "#c0392b"}
INTERVALO_MS = 2000


class VentanaPrincipal:
    """Ventana Tkinter. Solo muestra y pide cosas; la lógica está en modelo/."""

    def __init__(self, raiz):
        self.raiz = raiz
        self.sistema = SistemaMultiAgenteInundaciones()
        self.automatico = False
        self.tarea = None
        self.eventos_vistos = 0
        self.lista_mostrada = None
        self.alertas_mostradas = 0

        raiz.title("Sistema Multiagente de Inundaciones de Cartagena")
        izq = ttk.Frame(raiz, padding=8)
        izq.grid(row=0, column=0, sticky="ns")
        der = ttk.Frame(raiz, padding=8)
        der.grid(row=0, column=1, sticky="nsew")
        raiz.columnconfigure(1, weight=1)
        raiz.rowconfigure(0, weight=1)

        self.panel_simulacion(izq)
        self.panel_entorno(izq)
        self.panel_agentes(izq)
        self.pestanas(der)
        self.refrescar()

    # ---------- Paneles de la izquierda ----------
    def panel_simulacion(self, padre):
        f = ttk.LabelFrame(padre, text="Simulación", padding=6)
        f.pack(fill="x", pady=4)
        ttk.Label(f, text="Escenario:").grid(row=0, column=0, sticky="w")
        self.var_escenario = tk.StringVar(value="Normal")
        cb = ttk.Combobox(f, textvariable=self.var_escenario, state="readonly", width=16,
                          values=list(CiudadCartagena.ESCENARIOS))
        cb.grid(row=0, column=1, padx=4)
        cb.bind("<<ComboboxSelected>>", self.cambiar_escenario)
        ttk.Button(f, text="Siguiente ciclo", command=self.siguiente_ciclo).grid(
            row=1, column=0, columnspan=2, sticky="ew", pady=2)
        self.btn_auto = ttk.Button(f, text="Iniciar automático", command=self.alternar_automatico)
        self.btn_auto.grid(row=2, column=0, columnspan=2, sticky="ew", pady=2)
        self.var_aleatorio = tk.BooleanVar(value=False)
        ttk.Checkbutton(f, text="Fallos aleatorios", variable=self.var_aleatorio,
                        command=self.cambiar_aleatorio).grid(row=3, column=0, columnspan=2, sticky="w")

    def panel_entorno(self, padre):
        f = ttk.LabelFrame(padre, text="Entorno: CiudadCartagena", padding=6)
        f.pack(fill="x", pady=4)
        filas = [("ciclo", "Ciclo"), ("precipitacion", "Lluvia (mm/h)"),
                 ("alturaMarea", "Marea (m)"), ("nivelAgua", "Nivel de agua (cm)"),
                 ("reportes", "Reportes recibidos"), ("modo", "Valores")]
        self.etq = {}
        for i, (clave, texto) in enumerate(filas):
            ttk.Label(f, text=texto + ":").grid(row=i, column=0, sticky="w")
            self.etq[clave] = ttk.Label(f, text="-")
            self.etq[clave].grid(row=i, column=1, sticky="w", padx=6)
        n = len(filas)
        self.etq_riesgo = tk.Label(f, text="Bajo", fg="white", bg=COLORES["Bajo"],
                                   font=("Arial", 14, "bold"))
        self.etq_riesgo.grid(row=n, column=0, columnspan=2, sticky="ew", pady=4)

        m = ttk.Frame(f)
        m.grid(row=n + 1, column=0, columnspan=2)
        self.entradas_manual = []
        for i, (texto, defecto) in enumerate([("Lluvia", "0"), ("Marea", "0.2"), ("Agua", "0")]):
            ttk.Label(m, text=texto).grid(row=0, column=i)
            e = ttk.Entry(m, width=6)
            e.insert(0, defecto)
            e.grid(row=1, column=i, padx=2)
            self.entradas_manual.append(e)
        ttk.Button(f, text="Fijar valores manuales", command=self.fijar_manual).grid(
            row=n + 2, column=0, columnspan=2, sticky="ew", pady=2)
        ttk.Button(f, text="Volver a automático", command=self.volver_auto).grid(
            row=n + 3, column=0, columnspan=2, sticky="ew")

    def panel_agentes(self, padre):
        f = ttk.LabelFrame(padre, text="Agentes", padding=6)
        f.pack(fill="x", pady=4)
        self.etq_agente = {}
        self.btn_agente = {}
        for i, nombre in enumerate(self.sistema.agentes):
            ttk.Label(f, text=nombre).grid(row=i, column=0, sticky="w")
            etq = tk.Label(f, text="ACTIVO", fg="green", width=8)
            etq.grid(row=i, column=1)
            btn = ttk.Button(f, text="Fallar", width=10,
                             command=lambda n=nombre: self.alternar_fallo(n))
            btn.grid(row=i, column=2, padx=2)
            self.etq_agente[nombre] = etq
            self.btn_agente[nombre] = btn
        self.etq_alerta = tk.Label(f, text="", font=("Arial", 9, "bold"), wraplength=260)
        self.etq_alerta.grid(row=len(self.sistema.agentes), column=0, columnspan=3, pady=4)

    # ---------- Pestañas de la derecha ----------
    def pestanas(self, padre):
        nb = ttk.Notebook(padre)
        nb.pack(fill="both", expand=True)
        self.tab_ciudadano(nb)
        self.tab_operador(nb)
        self.tab_oagrd(nb)
        self.tab_umbrales(nb)
        self.tab_bitacora(nb)

    def tab_ciudadano(self, nb):
        t = ttk.Frame(nb, padding=10)
        nb.add(t, text="Ciudadano")
        ttk.Label(t, text="Barrio:").grid(row=0, column=0, sticky="w")
        self.c_barrio = ttk.Combobox(t, values=BARRIOS, state="readonly")
        self.c_barrio.current(0)
        self.c_barrio.grid(row=0, column=1, pady=3)
        ttk.Label(t, text="Categoría:").grid(row=1, column=0, sticky="w")
        self.c_cat = ttk.Combobox(t, values=CATEGORIAS, state="readonly")
        self.c_cat.current(0)
        self.c_cat.grid(row=1, column=1, pady=3)
        ttk.Button(t, text="Enviar reporte (WhatsApp)", command=self.enviar_reporte).grid(
            row=2, column=0, columnspan=2, sticky="ew", pady=3)
        ttk.Button(t, text="Consultar estado", command=self.consultar_estado).grid(
            row=3, column=0, columnspan=2, sticky="ew")
        self.c_resultado = ttk.Label(t, text="", wraplength=320)
        self.c_resultado.grid(row=4, column=0, columnspan=2, pady=8)

    def tab_operador(self, nb):
        t = ttk.Frame(nb, padding=10)
        nb.add(t, text="Operador")
        ttk.Label(t, text="Barrio:").grid(row=0, column=0, sticky="w")
        self.o_barrio = ttk.Combobox(t, values=BARRIOS, state="readonly")
        self.o_barrio.current(0)
        self.o_barrio.grid(row=0, column=1, pady=3)
        ttk.Label(t, text="Categoría:").grid(row=1, column=0, sticky="w")
        self.o_cat = ttk.Combobox(t, values=CATEGORIAS, state="readonly")
        self.o_cat.current(0)
        self.o_cat.grid(row=1, column=1, pady=3)
        ttk.Button(t, text="Registrar llamada", command=self.registrar_llamada).grid(
            row=2, column=0, columnspan=2, sticky="ew", pady=3)
        ttk.Button(t, text="Notificar emergencia (directo al Coordinador)",
                   command=self.notificar_emergencia).grid(row=3, column=0, columnspan=2, sticky="ew")

    def tab_oagrd(self, nb):
        t = ttk.Frame(nb, padding=10)
        nb.add(t, text="OAGRD")
        self.etq_oagrd = ttk.Label(t, text="Nivel de riesgo: -", font=("Arial", 11, "bold"))
        self.etq_oagrd.pack(anchor="w")
        ttk.Label(t, text="Lista de prioridades:").pack(anchor="w", pady=(8, 0))
        self.lb_lista = tk.Listbox(t, height=8, width=44, exportselection=False)
        self.lb_lista.pack(fill="x")
        ttk.Button(t, text="Marcar barrio seleccionado como Atendido",
                   command=self.atender).pack(fill="x", pady=4)
        ttk.Label(t, text="Alertas de emergencia:").pack(anchor="w", pady=(8, 0))
        self.lb_alertas = tk.Listbox(t, height=6, width=44, exportselection=False)
        self.lb_alertas.pack(fill="x")

    def tab_umbrales(self, nb):
        t = ttk.Frame(nb, padding=10)
        nb.add(t, text="Umbrales")
        ttk.Label(t, text="Supuestos académicos (no oficiales). Límite inferior de cada nivel.",
                  wraplength=320).grid(row=0, column=0, columnspan=4, pady=4)
        for j, nivel in enumerate(["moderada", "alta", "extrema"]):
            ttk.Label(t, text=nivel.capitalize()).grid(row=1, column=j + 1)
        nombres = {"lluvia": "Lluvia (mm/h)", "marea": "Marea (m)", "agua": "Agua (cm)"}
        self.entradas_umbral = {}
        for i, var in enumerate(["lluvia", "marea", "agua"]):
            ttk.Label(t, text=nombres[var]).grid(row=i + 2, column=0, sticky="w")
            for j, nivel in enumerate(["moderada", "alta", "extrema"]):
                e = ttk.Entry(t, width=7)
                e.insert(0, str(getattr(self.sistema.umbrales, var)[nivel]))
                e.grid(row=i + 2, column=j + 1, padx=3, pady=2)
                self.entradas_umbral[(var, nivel)] = e
        ttk.Button(t, text="Aplicar umbrales", command=self.aplicar_umbrales).grid(
            row=5, column=0, columnspan=4, sticky="ew", pady=8)

    def tab_bitacora(self, nb):
        t = ttk.Frame(nb, padding=6)
        nb.add(t, text="Bitácora")
        self.txt = tk.Text(t, height=24, width=60, state="disabled")
        barra = ttk.Scrollbar(t, command=self.txt.yview)
        self.txt.config(yscrollcommand=barra.set)
        self.txt.pack(side="left", fill="both", expand=True)
        barra.pack(side="right", fill="y")

    # ---------- Acciones ----------
    def log(self, texto):
        hora = datetime.now().strftime("%H:%M:%S")
        self.txt.config(state="normal")
        self.txt.insert("end", f"[{hora}] {texto}\n")
        self.txt.see("end")
        self.txt.config(state="disabled")

    def cambiar_escenario(self, _evento=None):
        self.sistema.entorno.escenario = self.var_escenario.get()
        self.sistema.entorno.volver_a_automatico()
        self.log(f"Escenario: {self.var_escenario.get()}")
        self.refrescar()

    def siguiente_ciclo(self):
        self.sistema.ejecutar_ciclo()
        self.refrescar()
        self.log(f"Ciclo {self.sistema.ciclo}: riesgo {self.sistema.coordinador.nivel_riesgo}")

    def alternar_automatico(self):
        self.automatico = not self.automatico
        if self.automatico:
            self.btn_auto.config(text="Pausar")
            self.bucle()
        else:
            self.btn_auto.config(text="Iniciar automático")
            if self.tarea:
                self.raiz.after_cancel(self.tarea)
                self.tarea = None

    def bucle(self):
        if self.automatico:
            self.siguiente_ciclo()
            self.tarea = self.raiz.after(INTERVALO_MS, self.bucle)

    def cambiar_aleatorio(self):
        self.sistema.modo_aleatorio = self.var_aleatorio.get()
        self.log("Fallos aleatorios: " + ("activados" if self.var_aleatorio.get() else "desactivados"))

    def fijar_manual(self):
        try:
            ll, ma, ag = (float(e.get().replace(",", ".")) for e in self.entradas_manual)
        except ValueError:
            messagebox.showerror("Dato inválido", "Escribe solo números.")
            return
        self.sistema.entorno.fijar_valores(ll, ma, ag)
        self.log(f"Valores manuales: lluvia={ll}, marea={ma}, agua={ag}")
        self.refrescar()

    def volver_auto(self):
        self.sistema.entorno.volver_a_automatico()
        self.log("Valores en modo automático")
        self.refrescar()

    def alternar_fallo(self, nombre):
        if self.sistema.agentes[nombre].activo:
            self.sistema.fallar(nombre)
            self.log(f"Fallo provocado en {nombre}")
        else:
            self.sistema.reactivar(nombre)
            self.log(f"{nombre} reactivado")
        self.refrescar()

    def enviar_reporte(self):
        barrio, cat = self.c_barrio.get(), self.c_cat.get()
        self.sistema.ciudadano.enviarReporte(barrio, cat)
        self.log(f"Ciudadano reportó {cat} en {barrio} (se procesa en el próximo ciclo)")

    def consultar_estado(self):
        barrio = self.c_barrio.get()
        r = self.sistema.ciudadano.consultarEstado(barrio)
        if r["en_lista"]:
            texto = f"{barrio} está en la lista de prioridades ({r['reportes']} reporte(s))."
        else:
            texto = f"{barrio} no está en la lista de prioridades."
        self.c_resultado.config(text=f"Riesgo actual de la ciudad: {r['nivel']}. {texto}")

    def registrar_llamada(self):
        barrio, cat = self.o_barrio.get(), self.o_cat.get()
        self.sistema.operador.registrarLlamada(barrio, cat)
        self.log(f"Operador registró llamada: {cat} en {barrio}")

    def notificar_emergencia(self):
        barrio = self.o_barrio.get()
        self.sistema.operador.notificarEmergencia(barrio)
        self.log(f"Operador notificó emergencia en {barrio}")

    def atender(self):
        sel = self.lb_lista.curselection()
        if not sel or not self.lista_mostrada:
            messagebox.showinfo("Selecciona un barrio", "Elige un barrio de la lista.")
            return
        barrio = self.lista_mostrada[sel[0]][0]
        self.sistema.oagrd.coordinarRespuesta(barrio)
        self.log(f"OAGRD marcó como atendido: {barrio}")
        self.refrescar()

    def aplicar_umbrales(self):
        nuevos = {}
        try:
            for var in ("lluvia", "marea", "agua"):
                m, a, x = (float(self.entradas_umbral[(var, n)].get().replace(",", "."))
                           for n in ("moderada", "alta", "extrema"))
                if not m < a < x:
                    messagebox.showerror("Umbral inválido",
                                         f"En {var}: moderada < alta < extrema.")
                    return
                nuevos[var] = {"moderada": m, "alta": a, "extrema": x}
        except ValueError:
            messagebox.showerror("Dato inválido", "Escribe solo números.")
            return
        for var, valores in nuevos.items():
            getattr(self.sistema.umbrales, var).update(valores)
        self.log("Umbrales actualizados")

    # ---------- Actualizar la pantalla ----------
    def refrescar(self):
        s = self.sistema
        e = s.consultarEstado()
        self.etq["ciclo"].config(text=e["ciclo"])
        self.etq["precipitacion"].config(text=e["precipitacion"])
        self.etq["alturaMarea"].config(text=e["alturaMarea"])
        self.etq["nivelAgua"].config(text=e["nivelAgua"])
        self.etq["reportes"].config(text=e["reportes"])
        self.etq["modo"].config(text="manuales" if e["manual"] else "automáticos")
        self.etq_riesgo.config(text=e["nivel"], bg=COLORES[e["nivel"]])

        for nombre, activo in e["agentes"].items():
            self.etq_agente[nombre].config(text="ACTIVO" if activo else "CAÍDO",
                                           fg="green" if activo else "red")
            self.btn_agente[nombre].config(text="Fallar" if activo else "Reactivar")
        if e["fallos"]:
            self.etq_alerta.config(text="FALLOS DETECTADOS: " + ", ".join(e["fallos"]), fg="red")
        else:
            self.etq_alerta.config(text="Supervisor: sin fallos detectados", fg="green")

        self.etq_oagrd.config(text=f"Nivel de riesgo: {e['nivel']}")
        if e["lista"] != self.lista_mostrada:
            self.lista_mostrada = e["lista"]
            self.lb_lista.delete(0, "end")
            for barrio, n in e["lista"]:
                self.lb_lista.insert("end", f"{barrio} - {n} reporte(s)")
        alertas = s.oagrd.alertas
        if len(alertas) != self.alertas_mostradas:
            self.alertas_mostradas = len(alertas)
            self.lb_alertas.delete(0, "end")
            for a in alertas:
                self.lb_alertas.insert("end", f"EMERGENCIA en {a['barrio']} (riesgo {a['nivel']})")

        for _hora, texto in s.supervisor.eventos[self.eventos_vistos:]:
            self.log(f"[Supervisor] {texto}")
        self.eventos_vistos = len(s.supervisor.eventos)
