import unittest
from src.proyecto_scheduler.proceso import Proceso
from src.proyecto_scheduler.fcfs_scheduler import FCFSScheduler
from src.proyecto_scheduler.round_robin_scheduler import RoundRobinScheduler
from src.proyecto_scheduler.repositorio import RepositorioProcesos

class TestScheduler(unittest.TestCase):

    def setUp(self):
        self.repositorio = RepositorioProcesos()
        self.proceso1 = Proceso(pid=1, duracion=5, prioridad=1, tiempo_llegada=0)
        self.proceso2 = Proceso(pid=2, duracion=3, prioridad=2, tiempo_llegada=1)
        self.proceso3 = Proceso(pid=3, duracion=2, prioridad=3, tiempo_llegada=2)
        self.repositorio.agregar_proceso(self.proceso1)
        self.repositorio.agregar_proceso(self.proceso2)
        self.repositorio.agregar_proceso(self.proceso3)

    def test_fcfs_scheduler(self):
        scheduler = FCFSScheduler(self.repositorio)
        orden_procesos = scheduler.planificar()
        self.assertEqual(orden_procesos[0].pid, 1)
        self.assertEqual(orden_procesos[1].pid, 2)
        self.assertEqual(orden_procesos[2].pid, 3)

    def test_round_robin_scheduler(self):
        scheduler = RoundRobinScheduler(self.repositorio, quantum=2)
        orden_procesos = scheduler.planificar()
        self.assertIn(orden_procesos[0].pid, [1, 2, 3])
        self.assertIn(orden_procesos[1].pid, [1, 2, 3])
        self.assertIn(orden_procesos[2].pid, [1, 2, 3])

if __name__ == '__main__':
    unittest.main()