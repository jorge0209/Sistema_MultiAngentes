import random

from modelo.entorno import CiudadCartagena
from modelo.umbrales import Umbrales
from modelo.roles import crear_roles
from modelo.actores import Ciudadano, OperadorEmergencias, OAGRD
from modelo.agentes.agente_lluvia import AgenteLluvia
from modelo.agentes.agente_mareas import AgenteMareas
from modelo.agentes.agente_evaluador_riesgo import AgenteEvaluadorRiesgo
from modelo.agentes.agente_reportes import AgenteReportes
from modelo.agentes.agente_coordinador import AgenteCoordinador
from modelo.agentes.agente_supervisor import AgenteSupervisor


class SistemaMultiAgenteInundaciones:
    """Organización: crea, es dueña de los agentes y ejecuta los ciclos."""

    PROBABILIDAD_FALLO = 0.15    # solo se usa en modo aleatorio

    def __init__(self):
        self.entorno = CiudadCartagena()
        self.umbrales = Umbrales()

        # Se crean en orden: cada agente necesita al que está "río abajo"
        self.oagrd = OAGRD()
        self.coordinador = AgenteCoordinador(self.oagrd)
        self.oagrd.coordinador = self.coordinador
        self.evaluador = AgenteEvaluadorRiesgo(self.entorno, self.umbrales, self.coordinador)
        self.lluvia = AgenteLluvia(self.entorno, self.umbrales, self.evaluador)
        self.mareas = AgenteMareas(self.entorno, self.umbrales, self.evaluador)
        self.reportes = AgenteReportes(self.entorno, self.coordinador)
        self.supervisor = AgenteSupervisor(
            [self.lluvia, self.mareas, self.evaluador, self.reportes, self.coordinador])

        # Agentes por nombre (para los botones de fallo) y orden del ciclo
        self.agentes = {a.nombre: a for a in [
            self.lluvia, self.mareas, self.evaluador,
            self.reportes, self.coordinador, self.supervisor]}
        self.orden = [self.lluvia, self.mareas, self.reportes,
                      self.evaluador, self.coordinador, self.supervisor]

        # Relación <<play>>: cada agente juega su rol
        self.roles = crear_roles()
        for agente in self.agentes.values():
            self.roles[agente.rol].asignar(agente)

        # Actores
        self.ciudadano = Ciudadano(self.reportes, self.coordinador)
        self.operador = OperadorEmergencias(self.reportes, self.coordinador)

        self.ciclo = 0
        self.modo_aleatorio = False

    def gestionarAgentes(self):
        """Da turno a cada agente, en el orden diseñado."""
        if self.modo_aleatorio and random.random() < self.PROBABILIDAD_FALLO:
            candidatos = [a for a in self.orden
                          if a.activo and a is not self.supervisor]
            if candidatos:
                random.choice(candidatos).activo = False
        for agente in self.orden:
            agente.ejecutar_ciclo()

    def coordinarAlertas(self):
        """La OAGRD procesa las alertas y listas que le llegaron."""
        self.oagrd.recibirAlertas()

    def ejecutar_ciclo(self):
        """Un ciclo completo de la simulación."""
        self.ciclo += 1
        self.entorno.generar_valores()
        self.gestionarAgentes()
        self.coordinarAlertas()

    def fallar(self, nombre: str):
        self.agentes[nombre].activo = False

    def reactivar(self, nombre: str):
        self.agentes[nombre].activo = True

    def consultarEstado(self) -> dict:
        """Resumen del estado general del sistema."""
        return {
            "ciclo": self.ciclo,
            "precipitacion": self.entorno.precipitacion,
            "alturaMarea": self.entorno.alturaMarea,
            "nivelAgua": self.entorno.nivelAgua,
            "reportes": self.entorno.reportesRecibidos,
            "manual": self.entorno.manual,
            "nivel": self.coordinador.nivel_riesgo,
            "lista": list(self.oagrd.lista),
            "agentes": {n: a.activo for n, a in self.agentes.items()},
            "fallos": [n for n, vivo in self.supervisor.estado.items() if not vivo],
        }
