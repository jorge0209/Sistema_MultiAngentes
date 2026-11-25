from modelo.mensaje import Mensaje

m = Mensaje("AgenteLluvia", "AgenteEvaluadorRiesgo", "medicion", {"valor": 42})
print(m)
print("Tipo:", m.tipo)
print("Valor:", m.contenido["valor"])