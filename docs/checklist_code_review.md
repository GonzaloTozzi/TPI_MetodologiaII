# Checklist de code review

Se aplicó sobre la versión inicial (tag `estado-inicial`) y sobre la versión refactorizada.

| N° | Criterio | Cómo se verifica | Versión inicial | Versión refactorizada |
|---|---|---|---|---|
| 1 | Las pruebas de comportamiento pasan | py -m pytest | Sí, 28 de 28 | Sí, las 22 de comportamiento sin modificar su archivo; 48 de 48 en total |
| 2 | Ninguna función supera complejidad ciclomática 10 | Flake8 C901 y Radon | No: main() tiene 14 | Sí: máximo 4 |
| 3 | Ninguna función tiene más de 5 parámetros | Pylint R0913 | No: registrar() tiene 6 | Sí |
| 4 | No hay código duplicado | Revisión manual | No: la lectura del ID está repetida | Sí |
| 5 | Estados y prioridades no están escritos a mano en varios lugares | Revisión manual | No: cuatro lugares | Sí: enumeraciones |
| 6 | Los nombres expresan la intención | Revisión manual | Parcial: s, asignar, filtrar | Sí |
| 7 | Interfaz, reglas y persistencia están separadas | Revisión de la estructura | No: un solo archivo | Sí: cuatro módulos y main.py |
| 8 | Las reglas de negocio no usan print ni input | Búsqueda en el código | No | Sí: solo consola.py y main.py |
| 9 | Cada error informa su causa | Pruebas de defectos | No: False genérico y archivo dañado sin controlar | Sí |
| 10 | Se validan todos los datos de entrada | Pruebas de defectos y unitarias | Parcial: nombre y descripción | Sí: también correo, tipo, prioridad y responsable |
| 11 | Pylint sin observaciones | py -m pylint | No: 8,19/10, 17 observaciones | Sí: 10,00/10 |
| 12 | Flake8 sin observaciones | py -m flake8 | No: 6 observaciones | Sí |
| 13 | Código documentado y README actualizado | Pylint y revisión del README | No | Sí |
| 14 | Las pruebas usan solo datos ficticios | Revisión de tests/datos_prueba.py | Sí | Sí |
| 15 | Se siguen leyendo los datos de la versión inicial | Prueba con un archivo creado por la versión inicial | No aplica | Sí: el formato del JSON no cambió |

## Observaciones registradas durante la revisión

| N° | Origen | Observación | Acción | Estado |
|---|---|---|---|---|
| 1 | Pylint | Faltaban docstrings en módulos, clases y métodos públicos (46 avisos). | Se documentaron módulos, clases y métodos públicos. | Corregida |
| 2 | Flake8 y Pylint | Las herramientas usaban límites de línea distintos (79 y 100): Flake8 marcaba 44 líneas que Pylint aceptaba. | Se unificó el límite en 100 con el archivo .flake8. | Corregida |
| 3 | Pylint | R0903 too-few-public-methods en Consola. | La consola expone a propósito un solo método público, ejecutar(); se dejó indicado en el código. | Aceptada con justificación |
| 4 | Revisión manual | La prueba unitaria de cambio de estado no detectaba si el servicio dejaba de guardar, porque el repositorio en memoria comparte los objetos con el servicio. | Se agregó el control de la cantidad de veces que se guarda, y se comprobó que la prueba falla al quitar el guardado. | Corregida |
| 5 | Revisión manual | La prueba de persistencia hacía todas las operaciones en una sola ejecución y ocultaba un guardado faltante. | Se separó en tres pruebas, una por operación. | Corregida |
| 6 | Revisión manual | Solicitud.desde_dict() no valida la prioridad. | Se mantiene así: los archivos creados con la versión inicial pueden tener cualquier prioridad y tienen que poder leerse. | Aceptada con justificación |
| 7 | Revisión manual | La validación del correo es básica. | Alcanza para el prototipo: controla usuario, arroba, dominio con punto y ausencia de espacios. | Aceptada con justificación |
| 8 | Revisión manual | El README describía la versión inicial (un solo archivo y diccionarios). | Se actualizó con estructura, instalación, uso, pruebas y tecnologías. | Corregida |

## Criterios de aceptación técnica

- Las 22 pruebas de comportamiento pasan sin modificar su archivo.
- Ninguna función supera complejidad ciclomática 10.
- Ninguna función tiene más de 5 parámetros.
- Pylint y Flake8 terminan sin observaciones con la configuración del repositorio.
- Solo consola.py y main.py interactúan con el usuario.
- Todo error que ve el usuario indica su causa.
- Los archivos de datos creados con la versión inicial se siguen pudiendo leer.
- El README permite instalar, usar y probar el sistema sin otra ayuda.

## Métricas antes y después

| Indicador | Versión inicial | Versión refactorizada |
|---|---|---|
| Archivos de código | 1 | 6 |
| Líneas de código (SLOC) | 97 | 306 |
| Complejidad ciclomática máxima (Radon) | 14, main() (C) | 4 (A) |
| Complejidad ciclomática promedio (Radon) | 4,1 | 1,9 |
| Funciones con más de 5 parámetros | 1, registrar() | 0 |
| Pylint, todas las reglas | 8,19/10 con 17 observaciones | 10,00/10 sin observaciones |
| Flake8 (línea máxima 100, complejidad máxima 10) | 6 observaciones | Sin observaciones |
| Pruebas automatizadas | 28 | 48 |
