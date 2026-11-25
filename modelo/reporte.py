from dataclasses import dataclass

CATEGORIAS = ["Inundación", "Incendio", "Derrumbe", "Otro"]
ORIGENES = ["WhatsApp", "Llamada"]
BARRIOS = [
    "Bocagrande", "Centro Histórico", "Getsemaní", "Manga",
    "El Bosque", "Olaya Herrera", "La Boquilla", "Crespo",
]


@dataclass
class Reporte:
    """Un reporte enviado por un ciudadano o registrado por el operador."""
    categoria: str
    origen: str
    barrio: str
