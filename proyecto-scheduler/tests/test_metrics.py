import pytest
from proyecto_scheduler.metrics import calcular_tiempo_respuesta, calcular_tiempo_retorno, calcular_tiempo_espera

def test_calcular_tiempo_respuesta():
    procesos = [
        {'pid': 1, 'tiempo_llegada': 0, 'duracion': 5},
        {'pid': 2, 'tiempo_llegada': 1, 'duracion': 3},
        {'pid': 3, 'tiempo_llegada': 2, 'duracion': 2},
    ]
    tiempos_respuesta = calcular_tiempo_respuesta(procesos)
    assert tiempos_respuesta[1] == 0  # Proceso 1
    assert tiempos_respuesta[2] == 4  # Proceso 2
    assert tiempos_respuesta[3] == 5  # Proceso 3

def test_calcular_tiempo_retorno():
    procesos = [
        {'pid': 1, 'tiempo_llegada': 0, 'duracion': 5},
        {'pid': 2, 'tiempo_llegada': 1, 'duracion': 3},
        {'pid': 3, 'tiempo_llegada': 2, 'duracion': 2},
    ]
    tiempos_retorno = calcular_tiempo_retorno(procesos)
    assert tiempos_retorno[1] == 5  # Proceso 1
    assert tiempos_retorno[2] == 7  # Proceso 2
    assert tiempos_retorno[3] == 7  # Proceso 3

def test_calcular_tiempo_espera():
    procesos = [
        {'pid': 1, 'tiempo_llegada': 0, 'duracion': 5},
        {'pid': 2, 'tiempo_llegada': 1, 'duracion': 3},
        {'pid': 3, 'tiempo_llegada': 2, 'duracion': 2},
    ]
    tiempos_espera = calcular_tiempo_espera(procesos)
    assert tiempos_espera[1] == 0  # Proceso 1
    assert tiempos_espera[2] == 4  # Proceso 2
    assert tiempos_espera[3] == 5  # Proceso 3