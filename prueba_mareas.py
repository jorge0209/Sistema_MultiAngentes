from modelo.entorno import CiudadCartagena
from modelo.umbrales import Umbrales
from modelo.agentes.agente_base import Agente
from modelo.agentes.agente_mareas import AgenteMareas

entorno = CiudadCartagena()
umbrales = Umbrales()
evaluador = Agente("AgenteEvaluadorRiesgo", "Basado en reglas", "EvaluadorRiesgo")  # provisional
mareas = AgenteMareas(entorno, umbrales, evaluador)

for altura in (0.2, 0.7, 0.9):
    entorno.fijar_valores(5, altura, 0)
    mareas.ejecutar_ciclo()
    for m in evaluador.leer_buzon():
        print(f"Marea {altura} m -> {m.emisor}: {m.contenido}")

mareas.activo = False
mareas.ejecutar_ciclo()
print("Buzón del evaluador con el agente caído:", evaluador.buzon)
