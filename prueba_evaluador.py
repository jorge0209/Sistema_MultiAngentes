from modelo.entorno import CiudadCartagena
from modelo.umbrales import Umbrales
from modelo.agentes.agente_base import Agente
from modelo.agentes.agente_lluvia import AgenteLluvia
from modelo.agentes.agente_mareas import AgenteMareas
from modelo.agentes.agente_evaluador_riesgo import AgenteEvaluadorRiesgo

entorno = CiudadCartagena()
umbrales = Umbrales()
coordinador = Agente("AgenteCoordinador", "Híbrido", "Priorizador")  # provisional
evaluador = AgenteEvaluadorRiesgo(entorno, umbrales, coordinador)
lluvia = AgenteLluvia(entorno, umbrales, evaluador)
mareas = AgenteMareas(entorno, umbrales, evaluador)

# (lluvia, marea, agua, nivel esperado)
casos = [
    (5, 0.2, 0, "Bajo"),
    (5, 0.7, 0, "Medio"),
    (35, 0.2, 0, "Medio"),
    (5, 0.2, 3, "Medio"),
    (35, 0.7, 0, "Alto"),
    (75, 0.2, 0, "Alto"),
    (5, 0.2, 15, "Alto"),
    (75, 0.9, 0, "Crítico"),
    (5, 0.2, 35, "Crítico"),
]

for lluv, mar, agua, esperado in casos:
    entorno.fijar_valores(lluv, mar, agua)
    lluvia.ejecutar_ciclo()
    mareas.ejecutar_ciclo()
    evaluador.ejecutar_ciclo()
    for m in coordinador.leer_buzon():
        nivel = m.contenido["nivel"]
        marca = "OK" if nivel == esperado else "ERROR"
        print(f"Lluvia {lluv}, marea {mar}, agua {agua} -> {nivel} (esperado {esperado}) {marca}")
