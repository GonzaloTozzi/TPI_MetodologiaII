# Sistema de Gestión de Solicitudes Académicas

Aplicación de consola en Python para registrar y gestionar solicitudes académicas: alta, listado, cambio de estado, asignación de responsable, filtrado por estado y reporte.

Trabajo Práctico Integrador de Metodología de Sistemas II (UTN, Tecnicatura Universitaria en Programación a Distancia). El repositorio conserva la versión inicial (tag `estado-inicial`) y la versión mejorada mediante refactoring (tag `estadorefactorizado`).

## Requisitos

- Python 3.9 o superior.
- El sistema no usa librerías externas.
- Para las pruebas y el análisis del código: pytest, Pylint, Flake8 y Radon.

## Instalación

```
git clone https://github.com/GonzaloTozzi/TPI_MetodologiaII.git
cd TPI_MetodologiaII
py -m pip install pytest pylint flake8 radon
```

En Linux o macOS se usa `python3` en lugar de `py`.

## Uso

```
py main.py
```

Los datos se guardan en `solicitudes.json`, en la carpeta desde la que se ejecuta el programa. El archivo se crea al registrar la primera solicitud. Usar solo datos ficticios.

## Funcionalidades

1. Registrar solicitud: estudiante, correo, tipo, descripción y prioridad (Baja, Media o Alta).
2. Listar solicitudes con su estado y su responsable.
3. Cambiar estado: Pendiente, En proceso o Resuelta.
4. Asignar responsable y área.
5. Filtrar por estado.
6. Reporte: total de solicitudes y cantidad por estado.

## Estructura

| Archivo | Responsabilidad |
|---|---|
| `main.py` | Arma las dependencias y arranca la consola |
| `consola.py` | Menú, lectura de datos y mensajes al usuario |
| `servicio.py` | Reglas de negocio |
| `repositorio.py` | Lectura y escritura del archivo JSON |
| `modelos.py` | Entidades, estados, prioridades y validaciones |
| `errores.py` | Errores propios del sistema |
| `tests/` | Pruebas automatizadas |
| `docs/` | Diagnóstico, decisiones técnicas, checklist de code review y evidencias |

## Pruebas y análisis

```
py -m pytest -v
py -m pylint main.py consola.py servicio.py repositorio.py modelos.py errores.py
py -m flake8
py -m radon cc -s -a main.py consola.py servicio.py repositorio.py modelos.py errores.py
```

- `tests/test_comportamiento.py`: comportamiento externo; se escribió sobre la versión inicial y no se modificó durante el refactoring.
- `tests/test_defectos_corregidos.py`: defectos visibles de la versión inicial, ya corregidos.
- `tests/test_unitarios_modelos.py` y `tests/test_unitarios_servicio.py`: pruebas unitarias.

## Tecnologías

Python 3, JSON, pytest, Pylint, Flake8, Radon, Git y GitHub.
