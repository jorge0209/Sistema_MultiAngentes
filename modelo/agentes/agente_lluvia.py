from modelo.agentes.agente_base import Agente


class AgenteLluvia(Agente):
    """Reactivo simple. Rol: VigilanteLluvia."""

    def __init__(self, entorno, umbrales, evaluador):
        super().__init__("AgenteLluvia", "Reactivo simple", "VigilanteLluvia")
        self.entorno = entorno
        self.umbrales = umbrales
        self.evaluador = evaluador

    def detectarLluviaAlta(self) -> bool:
        """Verdadero si la lluvia está en nivel Alta o Extrema."""
        nivel = self.umbrales.clasificar("lluvia", self.entorno.precipitacion)
        return nivel in ("alta", "extrema")

    def enviaralEvaluadorRiesgo(self):
        """Envía la medición y la marca 'alta' al evaluador."""
        medicion = {
            "variable": "lluvia",
            "valor": self.entorno.precipitacion,
            "alta": self.detectarLluviaAlta(),
        }
        self.enviar(self.evaluador, "medicion", medicion)

    def actuar(self):
        """Regla reactiva: percibo el entorno y reacciono enviando mi medición."""
        self.enviaralEvaluadorRiesgo()
