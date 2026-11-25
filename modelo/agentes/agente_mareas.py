from modelo.agentes.agente_base import Agente


class AgenteMareas(Agente):
    """Reactivo simple. Rol: VigilanteMareas."""

    def __init__(self, entorno, umbrales, evaluador):
        super().__init__("AgenteMareas", "Reactivo simple", "VigilanteMareas")
        self.entorno = entorno
        self.umbrales = umbrales
        self.evaluador = evaluador

    def detectarMareaAlta(self) -> bool:
        """Verdadero si la marea está en nivel Alta o Extrema."""
        nivel = self.umbrales.clasificar("marea", self.entorno.alturaMarea)
        return nivel in ("alta", "extrema")

    def enviaralEvaluadorRiesgo(self):
        """Envía la medición y la marca 'alta' al evaluador."""
        medicion = {
            "variable": "marea",
            "valor": self.entorno.alturaMarea,
            "alta": self.detectarMareaAlta(),
        }
        self.enviar(self.evaluador, "medicion", medicion)

    def actuar(self):
        """Regla reactiva: percibo el entorno y reacciono enviando mi medición."""
        self.enviaralEvaluadorRiesgo()
