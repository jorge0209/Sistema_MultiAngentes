class Umbrales:
    """Valores límite editables (supuestos académicos, no oficiales)."""

    def __init__(self):
        # Límite inferior de cada categoría
        self.lluvia = {"moderada": 10, "alta": 30, "extrema": 60}     # mm/h
        self.marea = {"moderada": 0.4, "alta": 0.6, "extrema": 0.8}   # metros
        self.agua = {"moderada": 1, "alta": 10, "extrema": 30}        # cm

    def clasificar(self, variable: str, valor: float) -> str:
        """Devuelve 'normal', 'moderada', 'alta' o 'extrema'."""
        limites = getattr(self, variable)
        if valor >= limites["extrema"]:
            return "extrema"
        if valor >= limites["alta"]:
            return "alta"
        if valor >= limites["moderada"]:
            return "moderada"
        return "normal"
