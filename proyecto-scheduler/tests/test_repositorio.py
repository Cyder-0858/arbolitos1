import unittest
from src.proyecto_scheduler.repositorio import RepositorioProcesos
from src.proyecto_scheduler.proceso import Proceso

class TestRepositorioProcesos(unittest.TestCase):

    def setUp(self):
        self.repositorio = RepositorioProcesos()

    def test_agregar_proceso(self):
        proceso = Proceso(pid=1, duracion=5, prioridad=1, tiempo_llegada=0)
        self.repositorio.agregar_proceso(proceso)
        self.assertIn(proceso, self.repositorio.listar_procesos())

    def test_listar_procesos(self):
        proceso1 = Proceso(pid=1, duracion=5, prioridad=1, tiempo_llegada=0)
        proceso2 = Proceso(pid=2, duracion=3, prioridad=2, tiempo_llegada=1)
        self.repositorio.agregar_proceso(proceso1)
        self.repositorio.agregar_proceso(proceso2)
        procesos = self.repositorio.listar_procesos()
        self.assertEqual(len(procesos), 2)
        self.assertIn(proceso1, procesos)
        self.assertIn(proceso2, procesos)

    def test_eliminar_proceso(self):
        proceso = Proceso(pid=1, duracion=5, prioridad=1, tiempo_llegada=0)
        self.repositorio.agregar_proceso(proceso)
        self.repositorio.eliminar_proceso(proceso.pid)
        self.assertNotIn(proceso, self.repositorio.listar_procesos())

    def test_obtener_proceso(self):
        proceso = Proceso(pid=1, duracion=5, prioridad=1, tiempo_llegada=0)
        self.repositorio.agregar_proceso(proceso)
        obtenido = self.repositorio.obtener_proceso(proceso.pid)
        self.assertEqual(obtenido, proceso)

if __name__ == '__main__':
    unittest.main()