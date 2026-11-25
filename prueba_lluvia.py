from modelo.entorno import CiudadCartagena
from modelo.umbrales import Umbrales
from modelo.agentes.agente_base import Agente
from modelo.agentes.agente_lluvia import AgenteLluvia

entorno = CiudadCartagena()
umbrales = Umbrales()
evaluador = Agente("AgenteEvaluadorRiesgo", "Basado en reglas", "EvaluadorRiesgo")  # provisional
lluvia = AgenteLluvia(entorno, umbrales, evaluador)

for llovizna in (5, 35, 75):
    entorno.fijar_valores(llovizna, 0.2, 0)
    lluvia.ejecutar_ciclo()
    for m in evaluador.leer_buzon():
        print(f"Lluvia {llovizna} mm -> {m.emisor}: {m.contenido}")

lluvia.activo = False
lluvia.ejecutar_ciclo()
print("Buzón del evaluador con el agente caído:", evaluador.buzon)
