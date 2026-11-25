from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Mensaje:
    """Carta que un agente deja en el buzón de otro agente."""
    emisor: str
    receptor: str
    tipo: str
    contenido: dict
    hora: str = field(default_factory=lambda: datetime.now().strftime("%H:%M:%S"))
