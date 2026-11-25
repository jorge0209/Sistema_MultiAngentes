import random


class CiudadCartagena:
    """Entorno donde habitan la organización y los agentes."""

    # Rangos de cada escenario (supuestos académicos aprobados)
    # formato: variable: (mínimo, máximo)
    ESCENARIOS = {
        "Normal":         {"precipitacion": (0, 9),   "alturaMarea": (0.1, 0.39), "nivelAgua": (0, 0)},
        "Lluvia intensa": {"precipitacion": (30, 80), "alturaMarea": (0.1, 0.39), "nivelAgua": (0, 9)},
        "Marea alta":     {"precipitacion": (0, 9),   "alturaMarea": (0.6, 1.0),  "nivelAgua": (0, 9)},
        "Inundación":     {"precipitacion": (60, 90), "alturaMarea": (0.6, 1.0),  "nivelAgua": (10, 40)},
    }

    def __init__(self):
        self.precipitacion = 0.0     # mm en 1 hora
        self.alturaMarea = 0.0       # metros
        self.nivelAgua = 0.0         # cm sobre la calle
        self.reportesRecibidos = 0   # cantidad de reportes
        self.escenario = "Normal"
        self.manual = False          # True = se usan los valores fijados a mano

    def generar_valores(self):
        """Genera valores aleatorios del escenario, salvo que estén fijados a mano."""
        if self.manual:
            return
        rangos = self.ESCENARIOS[self.escenario]
        self.precipitacion = round(random.uniform(*rangos["precipitacion"]), 1)
        self.alturaMarea = round(random.uniform(*rangos["alturaMarea"]), 2)
        self.nivelAgua = round(random.uniform(*rangos["nivelAgua"]), 1)

    def fijar_valores(self, precipitacion: float, alturaMarea: float, nivelAgua: float):
        """Control manual: el usuario fija los tres valores."""
        self.precipitacion = precipitacion
        self.alturaMarea = alturaMarea
        self.nivelAgua = nivelAgua
        self.manual = True

    def volver_a_automatico(self):
        """Deja de usar los valores manuales."""
        self.manual = False

    def registrar_reporte(self):
        """Suma un reporte recibido."""
        self.reportesRecibidos += 1
