from modelo.agentes.agente_base import Agente
from modelo.agentes.agente_supervisor import AgenteSupervisor

a = Agente("AgenteA", "Prueba", "Prueba")
b = Agente("AgenteB", "Prueba", "Prueba")
supervisor = AgenteSupervisor([a, b])

def ciclo():
    a.ejecutar_ciclo()
    b.ejecutar_ciclo()
    supervisor.ejecutar_ciclo()

ciclo()
print("Ciclo 1 (todos activos) - avisos:", supervisor.avisos)

b.activo = False
ciclo()
print("Ciclo 2 (B cae) - avisos:", supervisor.avisos)

ciclo()
print("Ciclo 3 (B sigue caído) - avisos:", len(supervisor.avisos), "aviso(s)")

b.activo = True
ciclo()
print("Ciclo 4 (B reactivado):")
for hora, texto in supervisor.eventos:
    print("  ", texto)
