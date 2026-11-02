# Documentación del Proyecto - Etapas 1, 2 y 3

## ETAPA 1: Selección y descripción del sistema base

### Selección y descripción del sistema base
Para el desarrollo de este trabajo práctico integrador se seleccionó como sistema base una aplicación de gestión de solicitudes académicas desarrollada en Python. El objetivo central del proyecto es contar con una herramienta operativa que permita evaluar la calidad interna del código, identificar deuda técnica y aplicar refactorings de forma segura sin alterar su comportamiento externo.

#### Actores del sistema
* **Estudiante:** actúa como el solicitante que requiere gestionar un trámite o consulta académica.
* **Personal administrativo / Operador de consola:** persona encargada de registrar las solicitudes, listar los trámites existentes, filtrar por estado, actualizar ciclos de vida y generar reportes globales.
* **Responsable / Área académica:** entidad o personal docente/administrativo asignado para resolver y dar seguimiento a una solicitud particular.

#### Estructuras y entidades principales
1. **Solicitud:** representa la petición realizada, conteniendo ID único, estudiante, correo de contacto, tipo de trámite, descripción, prioridad, estado y responsable asignado.
2. **Estudiante:** datos del solicitante (nombre y correo electrónico).
3. **Responsable:** datos de la persona o área técnica asignada a la atención del caso (nombre y área).

#### Tecnología utilizada
* **Lenguaje de programación:** Python 3.9 o superior (biblioteca estándar).
* **Persistencia:** archivos en formato JSON.
* **Control de versiones:** Git y GitHub.

---

## ETAPA 2: Calidad externa vs. calidad interna

### Calidad externa y defectos visibles
Desde el punto de vista operativo, la versión inicial cumple con las funcionalidades mínimas requeridas. Sin embargo, presenta defectos visibles documentados en `test_defectos_conocidos.py`:
* Formateo crudo en la presentación de responsables: `{'nombre': 'Laura Gómez', 'area': 'Alumnado'}`.
* Sensibilidad inconsistente a mayúsculas: "en proceso" en minúsculas falla y se rechaza.
* Sin retroalimentación en búsquedas de estado sin coincidencias.
* Mensajes de error ambiguos: "No se pudo actualizar." para ID inexistente o estado inválido.
* Prioridad acepta cualquier texto sin validar.
* Vulnerabilidad a un crash no controlado ante un archivo JSON dañado.

### Calidad interna y mantenibilidad
A nivel de código fuente, la calidad interna es deficiente debido a la estructura monolítica en `main.py`, donde conviven la consola, validaciones, reglas de negocio y persistencia en JSON.

### Ejemplo de impacto en la evolución futura
Agregar un estado "Rechazada" obliga a modificar manualmente tres puntos distintos de `main.py` (líneas 45, 72 y 98), multiplicando el riesgo de regresiones.

---

## ETAPA 3: Deuda técnica y code smells

### Diagnóstico de debilidades y Code Smells
1. **Módulo monolito:** `main.py` (líneas 1-120). Mezcla consola, negocio y persistencia.
2. **Long Method:** `main()` (líneas 76-116). Complejidad en el control del menú.
3. **Long Parameter List:** `registrar()` (línea 19). Firma con 6 argumentos dispersos.
4. **Duplicated Code:** `main()` (líneas 93-97, 101-105). Parseo repetido de IDs.
5. **Magic Strings & Sensibilidad:** Líneas 25, 45, 72, 98. Cadenas literales y fallo con minúsculas.
6. **Feature Envy / Formateo:** Líneas 30, 64, 70. Salidas de texto mezcladas en el negocio.
7. **Validación Incompleta y Manejo de Errores Deficiente:** Líneas 7-12, 21, 46, 58. Retornos `False` sin explicación y crash en JSON.
8. **Acoplamiento a Persistencia:** Invocaciones a `guardar()` en líneas 26, 51 y 60.
9. **Data Clumps:** Líneas 19 y 32. `estudiante` y `correo` siempre acoplados.