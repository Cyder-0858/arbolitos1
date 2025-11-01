from src.proyecto_scheduler.proceso import Proceso
import pytest

def test_crear_proceso():
    proceso = Proceso(pid=1, duracion=5, prioridad=1, tiempo_llegada=0)
    assert proceso.pid == 1
    assert proceso.duracion == 5
    assert proceso.prioridad == 1
    assert proceso.tiempo_restante == 5
    assert proceso.tiempo_llegada == 0
    assert proceso.tiempo_inicio is None
    assert proceso.tiempo_fin is None

def test_pid_unico():
    proceso1 = Proceso(pid=1, duracion=5, prioridad=1, tiempo_llegada=0)
    proceso2 = Proceso(pid=2, duracion=3, prioridad=2, tiempo_llegada=1)
    assert proceso1.pid != proceso2.pid

def test_tiempo_fin():
    proceso = Proceso(pid=1, duracion=5, prioridad=1, tiempo_llegada=0)
    proceso.tiempo_inicio = 2
    proceso.tiempo_fin = proceso.tiempo_inicio + proceso.duracion
    assert proceso.tiempo_fin == 7

def test_tiempo_restante():
    proceso = Proceso(pid=1, duracion=5, prioridad=1, tiempo_llegada=0)
    proceso.tiempo_inicio = 2
    proceso.tiempo_restante = proceso.duracion - (3 - proceso.tiempo_inicio)
    assert proceso.tiempo_restante == 4