from modelo.agentes.agente_base import Agente


class AgenteCoordinador(Agente):
    """Híbrido (reactivo + deliberativo). Rol: Priorizador."""

    def __init__(self, oagrd):
        super().__init__("AgenteCoordinador", "Híbrido", "Priorizador")
        self.oagrd = oagrd
        self.nivel_riesgo = "Bajo"       # último nivel recibido del evaluador
        self.conteo = {}                 # barrio -> reportes pendientes
        self.atendidos = set()           # barrios que la OAGRD ya atendió
        self.lista = []                  # lista de prioridades actual
        self.aviso_fallos = []           # reservado para uso futuro

    # ---- Parte reactiva ----
    def notificarNuevaEmergencia(self, barrio: str):
        """Avisa de inmediato a la OAGRD de una emergencia."""
        self.enviar(self.oagrd, "emergencia", {"barrio": barrio, "nivel": self.nivel_riesgo})

    # ---- Parte deliberativa ----
    def organizarPrioridades(self):
        """Ordena los barrios por cantidad de reportes (mayor primero)."""
        pendientes = [(b, n) for b, n in self.conteo.items() if b not in self.atendidos and n > 0]
        pendientes.sort(key=lambda par: par[1], reverse=True)
        self.lista = pendientes

    def enviarListaOAGRD(self):
        """Envía a la OAGRD la lista de prioridades y el nivel de riesgo."""
        self.enviar(self.oagrd, "lista_prioridades",
                    {"nivel": self.nivel_riesgo, "lista": list(self.lista)})

    def actualizarLista(self, barrio_atendido: str):
        """La OAGRD atendió un barrio: sale de la lista y su conteo se reinicia."""
        self.conteo[barrio_atendido] = 0
        self.atendidos.discard(barrio_atendido)   # un reporte nuevo lo reabre
        self.organizarPrioridades()

    def _registrar_reporte(self, barrio: str):
        self.conteo[barrio] = self.conteo.get(barrio, 0) + 1

    def actuar(self):
        """Lee el buzón: reacciona a las emergencias y delibera con lo demás."""
        mensajes = self.leer_buzon()

        # 1) Reactivo: las emergencias se notifican primero y de inmediato
        for m in mensajes:
            if m.tipo == "emergencia":
                barrio = m.contenido["barrio"]
                self._registrar_reporte(barrio)
                self.notificarNuevaEmergencia(barrio)

        # 2) Deliberativo: riesgo y reportes
        for m in mensajes:
            if m.tipo == "nivel_riesgo":
                self.nivel_riesgo = m.contenido["nivel"]
            elif m.tipo == "reporte":
                self._registrar_reporte(m.contenido["reporte"].barrio)

        self.organizarPrioridades()
        self.enviarListaOAGRD()
