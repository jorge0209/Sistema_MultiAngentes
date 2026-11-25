from modelo.agentes.agente_base import Agente

a = Agente("A", "Reactivo simple", "Rol A")
b = Agente("B", "Reactivo simple", "Rol B")

a.enviar(b, "medicion", {"valor": 42})
print("Buzón de B:", b.leer_buzon())
print("Buzón de B después de leerlo:", b.buzon)

b.ejecutar_ciclo()
print("Señal de vida de B activo:", b.senal_de_vida)

b.activo = False
b.ejecutar_ciclo()
print("Señal de vida de B caído:", b.senal_de_vida)

a.enviar(b, "medicion", {"valor": 99})
print("Buzón de B caído:", b.buzon)
