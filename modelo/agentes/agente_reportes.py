from modelo.agentes.agente_base import Agente
from modelo.reporte import Reporte


class AgenteReportes(Agente):
    """Reactivo basado en modelos. Rol: FiltroReportes."""

    def __init__(self, entorno, coordinador):
        super().__init__("AgenteReportes", "Reactivo basado en modelos", "FiltroReportes")
        self.entorno = entorno
        self.coordinador = coordinador
        # Modelo interno del mundo (la memoria del agente)
        self.aceptados = []        # reportes de inundación aceptados
        self.descartados = 0       # cuántos no eran de inundación
        self.por_barrio = {}       # barrio -> cantidad de reportes válidos
        self.pendientes = []       # reportes por enviar al coordinador en este ciclo

    def recibirReporte(self):
        """Lee el buzón y guarda los reportes recibidos."""
        reportes = []
        for m in self.leer_buzon():
            if m.tipo == "reporte":
                reportes.append(m.contenido["reporte"])
                self.entorno.registrar_reporte()
        return reportes

    def filtrarInundaciones(self, reportes: list[Reporte]) -> list[Reporte]:
        """Se queda solo con reportes de inundación y sin duplicados del ciclo."""
        validos = []
        vistos = set()
        for r in reportes:
            if r.categoria != "Inundación":
                self.descartados += 1
                continue
            clave = (r.barrio, r.categoria, r.origen)
            if clave in vistos:
                continue
            vistos.add(clave)
            validos.append(r)
            self.aceptados.append(r)
            self.por_barrio[r.barrio] = self.por_barrio.get(r.barrio, 0) + 1
        return validos

    def enviarAlCoordinador(self, validos: list[Reporte]):
        """Envía cada reporte válido al Coordinador."""
        for r in validos:
            self.enviar(self.coordinador, "reporte", {"reporte": r})

    def actuar(self):
        """Ciclo: recibir, filtrar y enviar los válidos."""
        reportes = self.recibirReporte()
        validos = self.filtrarInundaciones(reportes)
        self.enviarAlCoordinador(validos)
