from dataclasses import dataclass


@dataclass
class Rol:
    """Papel que juega un agente en el sistema (relación <<play>>)."""
    nombre: str
    capacidades: list
    jugador: object = None      # el agente que juega este rol

    def asignar(self, agente):
        """Un agente pasa a jugar este rol (solo si el nombre coincide)."""
        if agente.rol != self.nombre:
            raise ValueError(f"{agente.nombre} no puede jugar el rol {self.nombre}")
        self.jugador = agente


def crear_roles() -> dict:
    """Crea los 6 roles del diagrama, con sus capacidades."""
    return {
        "VigilanteLluvia": Rol("VigilanteLluvia", [
            "detectar lluvia alta y reportarla",
            "acceder a datos de lluvia"]),
        "VigilanteMareas": Rol("VigilanteMareas", [
            "detectar marea alta y reportarla",
            "acceder a datos de marea"]),
        "EvaluadorRiesgo": Rol("EvaluadorRiesgo", [
            "analizar condiciones ambientales",
            "determinar nivel de riesgo",
            "generar informe de riesgo"]),
        "Supervisor": Rol("Supervisor", [
            "monitorear agentes y registrar fallos",
            "acceder al estado de todos los agentes"]),
        "Priorizador": Rol("Priorizador", [
            "organizar prioridades",
            "actualizar la lista y notificar emergencias",
            "acceder a información de agentes y comunicarse con la OAGRD"]),
        "FiltroReportes": Rol("FiltroReportes", [
            "filtrar reportes de inundación y descartar otros desastres",
            "acceder a reportes de WhatsApp y llamadas registradas"]),
    }
