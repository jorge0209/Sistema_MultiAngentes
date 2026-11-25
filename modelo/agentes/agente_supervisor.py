from datetime import datetime
from modelo.agentes.agente_base import Agente


class AgenteSupervisor(Agente):
    """Reactivo basado en modelos. Rol: Supervisor."""

    def __init__(self, agentes):
        super().__init__("AgenteSupervisor", "Reactivo basado en modelos", "Supervisor")
        self.agentes = agentes                                   # los agentes a vigilar
        self.estado = {a.nombre: True for a in agentes}          # modelo: último estado conocido
        self.eventos = []                                        # bitácora (hora, texto)
        self.avisos = []                                         # alertas de fallo

    def registrarEventos(self, texto: str):
        """Guarda un evento en la bitácora con la hora."""
        hora = datetime.now().strftime("%H:%M:%S")
        self.eventos.append((hora, texto))

    def avisarFallos(self, nombre: str):
        """Deja una alerta de fallo para que la interfaz la muestre."""
        self.avisos.append(f"ALERTA: {nombre} dejó de responder")

    def monitorearAgentes(self):
        """Compara la señal de vida de cada agente con lo último que sabía."""
        for agente in self.agentes:
            estaba_vivo = self.estado[agente.nombre]
            esta_vivo = agente.senal_de_vida
            if estaba_vivo and not esta_vivo:
                self.registrarEventos(f"{agente.nombre} cayó")
                self.avisarFallos(agente.nombre)
            elif not estaba_vivo and esta_vivo:
                self.registrarEventos(f"{agente.nombre} se recuperó")
            self.estado[agente.nombre] = esta_vivo

    def actuar(self):
        """Cada ciclo revisa a los demás agentes."""
        self.monitorearAgentes()
