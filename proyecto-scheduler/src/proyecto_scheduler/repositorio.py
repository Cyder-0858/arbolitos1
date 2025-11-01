class RepositorioProcesos:
    def __init__(self):
        self.procesos = []

    def agregar_proceso(self, proceso):
        self.procesos.append(proceso)

    def listar_procesos(self):
        return self.procesos

    def eliminar_proceso(self, pid):
        self.procesos = [p for p in self.procesos if p.pid != pid]

    def obtener_proceso(self, pid):
        for proceso in self.procesos:
            if proceso.pid == pid:
                return proceso
        return None