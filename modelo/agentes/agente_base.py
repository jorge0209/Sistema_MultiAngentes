from modelo.mensaje import Mensaje


class Agente:
    """Clase base: todo agente tiene nombre, buzón, estado y señal de vida."""

    def __init__(self, nombre: str, arquitectura: str, rol: str):
        self.nombre = nombre
        self.arquitectura = arquitectura
        self.rol = rol
        self.activo = True
        self.senal_de_vida = False
        self.buzon: list[Mensaje] = []

    def recibir(self, mensaje: Mensaje):
        """Otro agente deja un mensaje en mi buzón."""
        if self.activo:
            self.buzon.append(mensaje)

    def enviar(self, receptor: "Agente", tipo: str, contenido: dict):
        """Dejo un mensaje en el buzón de otro agente."""
        mensaje = Mensaje(self.nombre, receptor.nombre, tipo, contenido)
        receptor.recibir(mensaje)
        return mensaje

    def leer_buzon(self) -> list[Mensaje]:
        """Saco todos los mensajes del buzón y lo dejo vacío."""
        mensajes = self.buzon
        self.buzon = []
        return mensajes

    def ejecutar_ciclo(self):
        """Cada ciclo: si estoy activo, dejo señal de vida y actúo."""
        if not self.activo:
            self.senal_de_vida = False
            return
        self.senal_de_vida = True
        self.actuar()

    def actuar(self):
        """Cada agente sobrescribe este método con su comportamiento."""
        pass
