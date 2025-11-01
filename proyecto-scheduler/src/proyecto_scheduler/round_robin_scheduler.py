class RoundRobinScheduler(Scheduler):
    def __init__(self, quantum):
        self.quantum = quantum

    def planificar(self, procesos):
        queue = procesos.copy()
        tiempo_actual = 0
        while queue:
            proceso = queue.pop(0)
            if proceso.tiempo_restante > self.quantum:
                tiempo_actual += self.quantum
                proceso.tiempo_restante -= self.quantum
                queue.append(proceso)
            else:
                tiempo_actual += proceso.tiempo_restante
                proceso.tiempo_fin = tiempo_actual
                proceso.tiempo_restante = 0
                proceso.tiempo_inicio = tiempo_actual - proceso.duracion

        return procesos