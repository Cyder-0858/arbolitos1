class Proceso:
    def __init__(self, pid, duracion, prioridad, tiempo_llegada):
        self.pid = pid
        self.duracion = duracion
        self.prioridad = prioridad
        self.tiempo_restante = duracion
        self.tiempo_llegada = tiempo_llegada
        self.tiempo_inicio = None
        self.tiempo_fin = None

    def __repr__(self):
        return f"Proceso(pid={self.pid}, duracion={self.duracion}, prioridad={self.prioridad}, " \
               f"tiempo_restante={self.tiempo_restante}, tiempo_llegada={self.tiempo_llegada}, " \
               f"tiempo_inicio={self.tiempo_inicio}, tiempo_fin={self.tiempo_fin})"

    def iniciar(self, tiempo_inicio):
        self.tiempo_inicio = tiempo_inicio

    def finalizar(self, tiempo_fin):
        self.tiempo_fin = tiempo_fin
        self.tiempo_restante = 0

    def actualizar_tiempo_restante(self, tiempo):
        self.tiempo_restante -= tiempo
        if self.tiempo_restante < 0:
            self.tiempo_restante = 0