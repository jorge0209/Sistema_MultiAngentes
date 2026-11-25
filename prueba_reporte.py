from modelo.reporte import Reporte, CATEGORIAS, ORIGENES, BARRIOS

r = Reporte("Inundación", "WhatsApp", "Manga")
print(r)
print("Barrio:", r.barrio)
print("Categorías permitidas:", CATEGORIAS)
print("Cantidad de barrios:", len(BARRIOS))
