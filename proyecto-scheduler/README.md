# Proyecto Scheduler

Este proyecto implementa un sistema de planificación de procesos en Python, utilizando los algoritmos First-Come, First-Served (FCFS) y Round-Robin. El sistema permite registrar, listar y simular procesos, así como almacenar datos de manera persistente en archivos CSV y JSON.

## Estructura del Proyecto

```
proyecto-scheduler
├── src
│   └── proyecto_scheduler
│       ├── __init__.py
│       ├── proceso.py
│       ├── scheduler.py
│       ├── fcfs_scheduler.py
│       ├── round_robin_scheduler.py
│       ├── repositorio.py
│       ├── metrics.py
│       └── main.py
├── tests
│   ├── __init__.py
│   ├── test_proceso.py
│   ├── test_scheduler.py
│   ├── test_repositorio.py
│   ├── test_metrics.py
│   └── data
│       ├── procesos.json
│       └── procesos.csv
├── requirements.txt
├── README.md
└── .gitignore
```

## Instalación

1. Clona el repositorio:
   ```
   git clone <url_del_repositorio>
   cd proyecto-scheduler
   ```

2. Instala las dependencias:
   ```
   pip install -r requirements.txt
   ```

## Uso

Para ejecutar el sistema de planificación, puedes utilizar el archivo `main.py` que proporciona una interfaz de línea de comandos. Desde allí, podrás agregar y listar procesos, seleccionar algoritmos de planificación y ejecutar simulaciones.

## Pruebas

El proyecto incluye pruebas unitarias para asegurar el correcto funcionamiento de las clases y algoritmos implementados. Para ejecutar las pruebas, utiliza el siguiente comando:

```
pytest
```

## Contribuciones

Las contribuciones son bienvenidas. Si deseas contribuir, por favor abre un issue o envía un pull request.

## Licencia

Este proyecto está bajo la Licencia MIT.