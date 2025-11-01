class FCFSScheduler(Scheduler):
    def __init__(self):
        self.procesos = []

    def agregar_proceso(self, proceso):
        self.procesos.append(proceso)

    def planificar(self):
        # Ordenar procesos por tiempo de llegada
        self.procesos.sort(key=lambda p: p.tiempo_llegada)
        tiempo_actual = 0
        for proceso in self.procesos:
            if tiempo_actual < proceso.tiempo_llegada:
                tiempo_actual = proceso.tiempo_llegada
            proceso.tiempo_inicio = tiempo_actual
            proceso.tiempo_fin = tiempo_actual + proceso.duracion
            tiempo_actual += proceso.duracion

    def listar_procesos(self):
        return [(p.pid, p.tiempo_inicio, p.tiempo_fin) for p in self.procesos]