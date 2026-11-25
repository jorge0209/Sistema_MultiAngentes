from modelo.entorno import CiudadCartagena

c = CiudadCartagena()
c.escenario = "Inundación"
c.generar_valores()
print("Inundación:", c.precipitacion, c.alturaMarea, c.nivelAgua)

c.fijar_valores(5, 0.2, 0)
c.generar_valores()
print("Manual:", c.precipitacion, c.alturaMarea, c.nivelAgua)

c.volver_a_automatico()
c.escenario = "Normal"
c.generar_valores()
print("Normal:", c.precipitacion, c.alturaMarea, c.nivelAgua)
