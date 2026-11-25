from modelo.umbrales import Umbrales

u = Umbrales()
print("Lluvia 5 mm:", u.clasificar("lluvia", 5))
print("Lluvia 35 mm:", u.clasificar("lluvia", 35))
print("Lluvia 70 mm:", u.clasificar("lluvia", 70))
print("Marea 0.5 m:", u.clasificar("marea", 0.5))
print("Agua 30 cm:", u.clasificar("agua", 30))

u.lluvia["alta"] = 20   # simulamos que el usuario edita el umbral
print("Lluvia 25 mm con umbral 20:", u.clasificar("lluvia", 25))
