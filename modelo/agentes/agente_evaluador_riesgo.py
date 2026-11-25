from modelo.agentes.agente_base import Agente


class AgenteEvaluadorRiesgo(Agente):
    """Basado en reglas. Rol: EvaluadorRiesgo."""

    def __init__(self, entorno, umbrales, coordinador):
        super().__init__("AgenteEvaluadorRiesgo", "Basado en reglas", "EvaluadorRiesgo")
        self.entorno = entorno
        self.umbrales = umbrales
        self.coordinador = coordinador
        self.mediciones = {"lluvia": 0.0, "marea": 0.0}   # últimas mediciones recibidas
        self.ultimo_nivel = None

    def recibirMediciones(self):
        """Lee el buzón y guarda las mediciones de lluvia y marea."""
        for m in self.leer_buzon():
            if m.tipo == "medicion":
                self.mediciones[m.contenido["variable"]] = m.contenido["valor"]

    def evaluarRiesgo(self) -> dict:
        """Clasifica cada variable: normal, moderada, alta o extrema."""
        return {
            "lluvia": self.umbrales.clasificar("lluvia", self.mediciones["lluvia"]),
            "marea": self.umbrales.clasificar("marea", self.mediciones["marea"]),
            "agua": self.umbrales.clasificar("agua", self.entorno.nivelAgua),
        }

    def determinarNivelRiesgo(self, niveles: dict) -> str:
        """Aplica las reglas aprobadas, de la más grave a la menos grave."""
        lluvia = niveles["lluvia"]
        marea = niveles["marea"]
        agua = niveles["agua"]
        marea_alta = marea in ("alta", "extrema")
        lluvia_alta = lluvia in ("alta", "extrema")

        if (lluvia == "extrema" and marea_alta) or agua == "extrema":
            return "Crítico"
        if (lluvia == "alta" and marea_alta) or lluvia == "extrema" or agua == "alta":
            return "Alto"
        if lluvia_alta or marea_alta or agua == "moderada":
            return "Medio"
        return "Bajo"

    def enviarResultado(self, nivel: str, niveles: dict):
        """Envía el nivel de riesgo al Coordinador."""
        self.ultimo_nivel = nivel
        self.enviar(self.coordinador, "nivel_riesgo", {"nivel": nivel, "detalle": niveles})

    def actuar(self):
        """Ciclo completo: recibir, evaluar, determinar y enviar."""
        self.recibirMediciones()
        niveles = self.evaluarRiesgo()
        nivel = self.determinarNivelRiesgo(niveles)
        self.enviarResultado(nivel, niveles)
