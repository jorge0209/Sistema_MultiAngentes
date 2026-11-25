from modelo.reporte import Reporte
from modelo.agentes.agente_base import Agente
from modelo.agentes.agente_coordinador import AgenteCoordinador

oagrd = Agente("OAGRD", "Actor", "Actor")            # provisional
coordinador = AgenteCoordinador(oagrd)
otro = Agente("Otro", "Prueba", "Prueba")            # provisional (emisor de mensajes)

# Ciclo 1: riesgo Alto, 2 reportes de Manga y 1 de Bocagrande
otro.enviar(coordinador, "nivel_riesgo", {"nivel": "Alto", "detalle": {}})
otro.enviar(coordinador, "reporte", {"reporte": Reporte("Inundación", "WhatsApp", "Manga")})
otro.enviar(coordinador, "reporte", {"reporte": Reporte("Inundación", "Llamada", "Manga")})
otro.enviar(coordinador, "reporte", {"reporte": Reporte("Inundación", "WhatsApp", "Bocagrande")})
coordinador.ejecutar_ciclo()
print("Mensajes de la OAGRD (ciclo 1):")
for m in oagrd.leer_buzon():
    print("  ", m.tipo, m.contenido)

# Ciclo 2: emergencia directa del Operador en Crespo
otro.enviar(coordinador, "emergencia", {"barrio": "Crespo"})
coordinador.ejecutar_ciclo()
print("Mensajes de la OAGRD (ciclo 2):")
for m in oagrd.leer_buzon():
    print("  ", m.tipo, m.contenido)

# La OAGRD atiende Manga
coordinador.actualizarLista("Manga")
print("Lista tras atender Manga:", coordinador.lista)
