def calcular_tiempo_respuesta(procesos):
    for i, proceso in enumerate(procesos):
        if i == 0:
            proceso.tiempo_respuesta = proceso.tiempo_inicio
        else:
            proceso.tiempo_respuesta = procesos[i-1].tiempo_fin - proceso.tiempo_llegada

def calcular_tiempo_retorno(procesos):
    for proceso in procesos:
        proceso.tiempo_retorno = proceso.tiempo_fin - proceso.tiempo_llegada

def calcular_tiempo_espera(procesos):
    for proceso in procesos:
        proceso.tiempo_espera = proceso.tiempo_respuesta - proceso.duracion

def generar_diagrama_gantt(procesos):
    gantt = []
    for proceso in procesos:
        gantt.append((proceso.pid, proceso.tiempo_inicio, proceso.tiempo_fin))
    return gantt