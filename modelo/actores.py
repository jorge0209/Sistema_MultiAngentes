from modelo.mensaje import Mensaje
from modelo.reporte import Reporte


class Actor:
    """Clase base de los actores externos: tienen buzón, pero no son agentes."""

    def __init__(self, nombre: str):
        self.nombre = nombre
        self.buzon = []

    def recibir(self, mensaje: Mensaje):
        self.buzon.append(mensaje)

    def enviar(self, receptor, tipo: str, contenido: dict):
        mensaje = Mensaje(self.nombre, receptor.nombre, tipo, contenido)
        receptor.recibir(mensaje)
        return mensaje

    def leer_buzon(self) -> list:
        mensajes = self.buzon
        self.buzon = []
        return mensajes


class Ciudadano(Actor):
    """Envía reportes por WhatsApp y consulta el estado de la ciudad."""

    def __init__(self, agente_reportes, coordinador):
        super().__init__("Ciudadano")
        self.agente_reportes = agente_reportes
        self.coordinador = coordinador

    def enviarReporte(self, barrio: str, categoria: str):
        reporte = Reporte(categoria, "WhatsApp", barrio)
        self.enviar(self.agente_reportes, "reporte", {"reporte": reporte})

    def consultarEstado(self, barrio: str) -> dict:
        lista = dict(self.coordinador.lista)
        return {
            "nivel": self.coordinador.nivel_riesgo,
            "en_lista": barrio in lista,
            "reportes": lista.get(barrio, 0),
        }


class OperadorEmergencias(Actor):
    """Registra llamadas (pasan por el filtro) y notifica emergencias (atajo)."""

    def __init__(self, agente_reportes, coordinador):
        super().__init__("OperadorEmergencias")
        self.agente_reportes = agente_reportes
        self.coordinador = coordinador

    def registrarLlamada(self, barrio: str, categoria: str):
        reporte = Reporte(categoria, "Llamada", barrio)
        self.enviar(self.agente_reportes, "reporte", {"reporte": reporte})

    def notificarEmergencia(self, barrio: str):
        self.enviar(self.coordinador, "emergencia", {"barrio": barrio})


class OAGRD(Actor):
    """Recibe alertas y listas de prioridades; coordina la respuesta."""

    def __init__(self):
        super().__init__("OAGRD")
        self.coordinador = None      # se conecta al crear la organización
        self.nivel = "Bajo"
        self.lista = []
        self.alertas = []
        self.registro = []

    def recibirAlertas(self):
        for m in self.leer_buzon():
            if m.tipo == "emergencia":
                self.alertas.append(m.contenido)
            elif m.tipo == "lista_prioridades":
                self.nivel = m.contenido["nivel"]
                self.lista = m.contenido["lista"]

    def coordinarRespuesta(self, barrio: str):
        """Marca un barrio como atendido: sale de la lista de prioridades."""
        self.coordinador.actualizarLista(barrio)
        self.lista = [(b, n) for b, n in self.lista if b != barrio]
        self.registro.append(f"Barrio atendido: {barrio}")
