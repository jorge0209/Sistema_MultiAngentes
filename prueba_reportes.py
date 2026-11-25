from modelo.entorno import CiudadCartagena
from modelo.reporte import Reporte
from modelo.agentes.agente_base import Agente
from modelo.agentes.agente_reportes import AgenteReportes

entorno = CiudadCartagena()
coordinador = Agente("AgenteCoordinador", "Híbrido", "Priorizador")  # provisional
reportes = AgenteReportes(entorno, coordinador)
ciudadano = Agente("Ciudadano", "Actor", "Actor")  # provisional

envios = [
    Reporte("Inundación", "WhatsApp", "Manga"),
    Reporte("Incendio", "Llamada", "Crespo"),
    Reporte("Inundación", "WhatsApp", "Manga"),   # duplicado del mismo ciclo
    Reporte("Inundación", "Llamada", "Bocagrande"),
]
for r in envios:
    ciudadano.enviar(reportes, "reporte", {"reporte": r})

reportes.ejecutar_ciclo()
print("Llegaron al Coordinador:")
for m in coordinador.leer_buzon():
    print("  ", m.contenido["reporte"])

print("Aceptados:", len(reportes.aceptados))
print("Descartados:", reportes.descartados)
print("Por barrio:", reportes.por_barrio)
print("reportesRecibidos del entorno:", entorno.reportesRecibidos)

# Segundo ciclo: el mismo barrio vuelve a reportar y SÍ debe contarse
ciudadano.enviar(reportes, "reporte", {"reporte": Reporte("Inundación", "WhatsApp", "Manga")})
reportes.ejecutar_ciclo()
print("Por barrio tras el 2.º ciclo:", reportes.por_barrio)
