# CLI para gestionar procesos y ejecutar planificaciones (FCFS / Round-Robin).
import sys
import os
import json
import csv
from typing import List, Tuple, Dict, Any

# Añadir src/ al path si existe
ROOT = os.path.dirname(__file__)
SRC = os.path.join(ROOT, "src")
if os.path.isdir(SRC) and SRC not in sys.path:
    sys.path.insert(0, SRC)

# Intentar importar implementaciones del proyecto
try:
    from proceso import Proceso  # type: ignore
    from repositorio import RepositorioProcesos  # type: ignore
    from scheduler import FCFSScheduler, RoundRobinScheduler  # type: ignore
    try:
        from metrics import calcular_metricas  # type: ignore
    except Exception:
        calcular_metricas = None
except Exception:
    # Fallbacks para permitir uso del CLI sin módulos externos
    class Proceso:
        def __init__(self, pid: str, duracion: int, prioridad: int = 0):
            self.pid = str(pid)
            self.duracion = int(duracion)
            self.prioridad = int(prioridad)
            self.tiempo_restante = int(duracion)
            self.tiempo_llegada = 0
            self.tiempo_inicio = None
            self.tiempo_fin = None

        def to_dict(self):
            return {"pid": self.pid, "duracion": self.duracion, "prioridad": self.prioridad}

    class RepositorioProcesos:
        def __init__(self):
            self._proc: Dict[str, Proceso] = {}

        def agregar(self, p: Proceso):
            if p.pid in self._proc:
                raise ValueError("PID duplicado")
            self._proc[p.pid] = p

        def listar(self) -> List[Proceso]:
            return list(self._proc.values())

        def obtener(self, pid: str) -> Any:
            return self._proc.get(pid)

        def eliminar(self, pid: str):
            self._proc.pop(pid, None)

        def guardar_json(self, path: str):
            with open(path, "w", encoding="utf-8") as f:
                json.dump([p.to_dict() for p in self.listar()], f, indent=2, ensure_ascii=False)

        def cargar_json(self, path: str):
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            self._proc = {}
            for d in data:
                p = Proceso(d["pid"], int(d["duracion"]), int(d.get("prioridad", 0)))
                self._proc[p.pid] = p

        def guardar_csv(self, path: str):
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f, delimiter=";")
                writer.writerow(["pid", "duracion", "prioridad"])
                for p in self.listar():
                    writer.writerow([p.pid, p.duracion, p.prioridad])

        def cargar_csv(self, path: str):
            with open(path, encoding="utf-8") as f:
                reader = csv.DictReader(f, delimiter=";")
                self._proc = {}
                for r in reader:
                    p = Proceso(r["pid"], int(r["duracion"]), int(r.get("prioridad", 0)))
                    self._proc[p.pid] = p

    class FCFSScheduler:
        def planificar(self, procesos: List[Proceso]) -> List[Tuple[str, int, int]]:
            t = 0
            gantt: List[Tuple[str, int, int]] = []
            for p in procesos:
                start = t
                end = t + p.duracion
                gantt.append((p.pid, start, end))
                t = end
            return gantt

    class RoundRobinScheduler:
        def __init__(self, quantum: int = 1):
            self.quantum = max(1, int(quantum))

        def planificar(self, procesos: List[Proceso]) -> List[Tuple[str, int, int]]:
            t = 0
            gantt: List[Tuple[str, int, int]] = []
            # clonar duraciones para no mutar objetos originales
            queue = [Proceso(p.pid, p.duracion, getattr(p, "prioridad", 0)) for p in procesos]
            while any(p.duracion > 0 for p in queue):
                for p in queue:
                    if p.duracion <= 0:
                        continue
                    run = min(self.quantum, p.duracion)
                    start = t
                    t += run
                    p.duracion -= run
                    gantt.append((p.pid, start, t))
            return gantt

    calcular_metricas = None

def elegir_metodo(obj: Any, opciones: List[str]):
    for name in opciones:
        if hasattr(obj, name):
            return getattr(obj, name)
    return None

def imprimir_procesos(lista: List[Any]):
    if not lista:
        print("No hay procesos.")
        return
    print("PID\tDuracion\tPrioridad")
    for p in lista:
        pid = getattr(p, "pid", "?")
        dur = getattr(p, "duracion", "?")
        prio = getattr(p, "prioridad", "?")
        print(f"{pid}\t{dur}\t\t{prio}")

def calcular_metricas_simple(gantt: List[Tuple[str, int, int]], procesos: List[Any]) -> Dict[str, Any]:
    # tiempo_llegada asumido 0
    dur_map: Dict[str, int] = {}
    for p in procesos:
        pid = getattr(p, "pid", None)
        dur = getattr(p, "duracion", None)
        if pid is None:
            continue
        if dur is None:
            dur = sum(e - s for (pp, s, e) in gantt if pp == pid)
        dur_map[pid] = int(dur)

    inicio: Dict[str, int] = {}
    fin: Dict[str, int] = {}
    for pid, s, e in gantt:
        if pid not in inicio:
            inicio[pid] = s
        fin[pid] = e

    results: Dict[str, Dict[str, int]] = {}
    tiempos_resp: List[int] = []
    tiempos_espera: List[int] = []
    tiempos_retorno: List[int] = []
    for pid, d in dur_map.items():
        t_inicio = inicio.get(pid, 0)
        t_fin = fin.get(pid, 0)
        t_resp = t_inicio
        t_retorno = t_fin
        t_espera = t_retorno - d
        results[pid] = {"response": t_resp, "turnaround": t_retorno, "wait": t_espera}
        tiempos_resp.append(t_resp)
        tiempos_espera.append(t_espera)
        tiempos_retorno.append(t_retorno)

    avg = lambda arr: sum(arr) / len(arr) if arr else 0
    return {
        "por_proceso": results,
        "promedio_response": avg(tiempos_resp),
        "promedio_wait": avg(tiempos_espera),
        "promedio_turnaround": avg(tiempos_retorno),
    }

def main():
    repo = RepositorioProcesos()
    algoritmo = "fcfs"
    rr_quantum = 2

    while True:
        print("\n--- Scheduler CLI ---")
        print("1) Agregar proceso")
        print("2) Listar procesos")
        print("3) Seleccionar algoritmo (actual: {})".format(f"RR q={rr_quantum}" if algoritmo == "rr" else "FCFS"))
        print("4) Ejecutar simulación")
        print("5) Guardar procesos (.json/.csv)")
        print("6) Cargar procesos (.json/.csv)")
        print("0) Salir")
        opt = input("Opción: ").strip()

        if opt == "1":
            pid = input("PID: ").strip()
            try:
                dur = int(input("Duración (int >0): ").strip())
                prio = int(input("Prioridad (int, menor = más urgente): ").strip())
            except Exception:
                print("Entrada inválida.")
                continue
            p = Proceso(pid, dur, prio)
            try:
                fn = elegir_metodo(repo, ["agregar", "add", "add_proceso"])
                if fn:
                    fn(p)
                elif hasattr(repo, "_proc"):
                    repo._proc[pid] = p
                else:
                    raise RuntimeError("Repositorio no acepta agregar.")
                print("Proceso agregado.")
            except Exception as e:
                print("Error:", e)

        elif opt == "2":
            fn = elegir_metodo(repo, ["listar", "list", "get_all"])
            procesos = fn() if fn else list(getattr(repo, "_proc", {}).values())
            imprimir_procesos(procesos)

        elif opt == "3":
            c = input("1) FCFS  2) Round-Robin: ").strip()
            if c == "1":
                algoritmo = "fcfs"
                print("FCFS seleccionado.")
            elif c == "2":
                algoritmo = "rr"
                try:
                    rr_quantum = max(1, int(input("Quantum (int >0): ").strip()))
                except Exception:
                    rr_quantum = 2
                print(f"Round-Robin seleccionado (q={rr_quantum}).")
            else:
                print("Opción inválida.")

        elif opt == "4":
            fn = elegir_metodo(repo, ["listar", "list", "get_all"])
            procesos = fn() if fn else list(getattr(repo, "_proc", {}).values())
            if not procesos:
                print("No hay procesos para simular.")
                continue
            sched = FCFSScheduler() if algoritmo == "fcfs" else RoundRobinScheduler(rr_quantum)
            try:
                gantt = sched.planificar(procesos)
            except Exception as e:
                print("Error en planificación:", e)
                continue
            print("\nGantt (pid, inicio, fin):")
            for e in gantt:
                print(e)
            if calcular_metricas:
                try:
                    metrics = calcular_metricas(gantt, procesos)
                except Exception:
                    metrics = calcular_metricas_simple(gantt, procesos)
            else:
                metrics = calcular_metricas_simple(gantt, procesos)
            print("\nMétricas promedio:")
            print("Tiempo de respuesta:", metrics.get("promedio_response"))
            print("Tiempo de espera   :", metrics.get("promedio_wait"))
            print("Tiempo de retorno :", metrics.get("promedio_turnaround"))

        elif opt == "5":
            path = input("Guardar en (ruta .json/.csv): ").strip()
            if not path:
                print("Ruta inválida.")
                continue
            try:
                if path.lower().endswith(".json"):
                    fn = elegir_metodo(repo, ["guardar_json", "save_json", "save"])
                    if fn:
                        fn(path)
                    else:
                        procs = elegir_metodo(repo, ["listar", "list"])()
                        with open(path, "w", encoding="utf-8") as f:
                            json.dump([getattr(p, "to_dict", lambda: {"pid": p.pid, "duracion": p.duracion, "prioridad": getattr(p, "prioridad", 0)})() for p in procs], f, indent=2, ensure_ascii=False)
                elif path.lower().endswith(".csv"):
                    fn = elegir_metodo(repo, ["guardar_csv", "save_csv"])
                    if fn:
                        fn(path)
                    else:
                        procs = elegir_metodo(repo, ["listar", "list"])()
                        with open(path, "w", newline="", encoding="utf-8") as f:
                            w = csv.writer(f, delimiter=";")
                            w.writerow(["pid", "duracion", "prioridad"])
                            for p in procs:
                                w.writerow([p.pid, p.duracion, getattr(p, "prioridad", 0)])
                else:
                    print("Extensión no soportada.")
                    continue
                print("Guardado:", path)
            except Exception as e:
                print("Error guardando:", e)

        elif opt == "6":
            path = input("Cargar desde (ruta .json/.csv): ").strip()
            if not os.path.exists(path):
                print("Archivo no existe.")
                continue
            try:
                if path.lower().endswith(".json"):
                    fn = elegir_metodo(repo, ["cargar_json", "load_json", "load"])
                    if fn:
                        fn(path)
                    else:
                        repo.cargar_json(path)
                elif path.lower().endswith(".csv"):
                    fn = elegir_metodo(repo, ["cargar_csv", "load_csv"])
                    if fn:
                        fn(path)
                    else:
                        repo.cargar_csv(path)
                else:
                    print("Extensión no soportada.")
                    continue
                print("Cargado desde:", path)
            except Exception as e:
                print("Error cargando:", e)

        elif opt == "0":
            print("Saliendo.")
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    main()