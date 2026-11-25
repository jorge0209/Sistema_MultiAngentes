from modelo.roles import crear_roles
from modelo.agentes.agente_base import Agente

roles = crear_roles()
print("Roles creados:", len(roles))
print("VigilanteLluvia:", roles["VigilanteLluvia"].capacidades)

lluvia = Agente("AgenteLluvia", "Reactivo simple", "VigilanteLluvia")
roles["VigilanteLluvia"].asignar(lluvia)
print("Jugador:", roles["VigilanteLluvia"].jugador.nombre)

try:
    roles["Supervisor"].asignar(lluvia)
except ValueError as e:
    print("Error esperado:", e)
