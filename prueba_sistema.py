from modelo.organizacion import SistemaMultiAgenteInundaciones

s = SistemaMultiAgenteInundaciones()

print("== 1. Escenarios ==")
for esc in ["Normal", "Lluvia intensa", "Marea alta", "Inundación"]:
    s.entorno.escenario = esc
    s.ejecutar_ciclo()
    e = s.consultarEstado()
    print(f"{esc}: lluvia={e['precipitacion']} marea={e['alturaMarea']} "
          f"agua={e['nivelAgua']} -> {e['nivel']}")

print("== 2. Reportes y OAGRD ==")
s.entorno.fijar_valores(75, 0.9, 0)
s.ciudadano.enviarReporte("Manga", "Inundación")
s.ciudadano.enviarReporte("Crespo", "Incendio")
s.operador.registrarLlamada("Bocagrande", "Inundación")
s.ejecutar_ciclo()
s.ciudadano.enviarReporte("Manga", "Inundación")
s.ejecutar_ciclo()
print("Lista de la OAGRD:", s.oagrd.lista)
print("Descartados:", s.reportes.descartados)
print("reportesRecibidos:", s.entorno.reportesRecibidos)
print("Estado para el ciudadano (Manga):", s.ciudadano.consultarEstado("Manga"))

s.operador.notificarEmergencia("Crespo")
s.ejecutar_ciclo()
print("Alertas de la OAGRD:", s.oagrd.alertas)
print("Lista tras emergencia:", s.oagrd.lista)

s.oagrd.coordinarRespuesta("Manga")
print("Lista tras atender Manga:", s.oagrd.lista)
print("Registro OAGRD:", s.oagrd.registro)

print("== 3. Fallo de agente ==")
s.fallar("AgenteMareas")
s.ejecutar_ciclo()
print("Fallos detectados:", s.consultarEstado()["fallos"])
print("Avisos:", s.supervisor.avisos)
s.reactivar("AgenteMareas")
s.ejecutar_ciclo()
print("Bitácora del Supervisor:", [t for h, t in s.supervisor.eventos])
