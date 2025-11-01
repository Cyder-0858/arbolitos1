# filepath: /proyecto-scheduler/proyecto-scheduler/src/proyecto_scheduler/main.py

import json
import csv
import os
from proceso import Proceso
from repositorio import RepositorioProcesos
from fcfs_scheduler import FCFSScheduler
from round_robin_scheduler import RoundRobinScheduler

def cargar_procesos_json(ruta):
    with open(ruta, 'r') as archivo:
        return json.load(archivo)

def cargar_procesos_csv(ruta):
    procesos = []
    with open(ruta, 'r') as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            procesos.append(Proceso(
                pid=int(fila['pid']),
                duracion=int(fila['duracion']),
                prioridad=int(fila['prioridad']),
                tiempo_llegada=int(fila['tiempo_llegada'])
            ))
    return procesos

def main():
    repositorio = RepositorioProcesos()
    
    # Cargar procesos desde archivos
    if os.path.exists('tests/data/procesos.json'):
        procesos_json = cargar_procesos_json('tests/data/procesos.json')
        for p in procesos_json:
            repositorio.agregar_proceso(Proceso(**p))
    
    if os.path.exists('tests/data/procesos.csv'):
        procesos_csv = cargar_procesos_csv('tests/data/procesos.csv')
        for p in procesos_csv:
            repositorio.agregar_proceso(p)

    while True:
        print("1. Listar procesos")
        print("2. Agregar proceso")
        print("3. Ejecutar planificación FCFS")
        print("4. Ejecutar planificación Round Robin")
        print("5. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            for proceso in repositorio.listar_procesos():
                print(proceso)

        elif opcion == '2':
            pid = int(input("Ingrese PID: "))
            duracion = int(input("Ingrese duración: "))
            prioridad = int(input("Ingrese prioridad: "))
            tiempo_llegada = int(input("Ingrese tiempo de llegada: "))
            nuevo_proceso = Proceso(pid, duracion, prioridad, tiempo_llegada)
            repositorio.agregar_proceso(nuevo_proceso)

        elif opcion == '3':
            scheduler = FCFSScheduler(repositorio.listar_procesos())
            scheduler.planificar()

        elif opcion == '4':
            quantum = int(input("Ingrese el quantum: "))
            scheduler = RoundRobinScheduler(repositorio.listar_procesos(), quantum)
            scheduler.planificar()

        elif opcion == '5':
            break

if __name__ == "__main__":
    main()