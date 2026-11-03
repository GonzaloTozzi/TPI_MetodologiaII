# Etapas 1, 2 y 3

## Etapa 1: Selección y descripción del sistema base

Se trabajó sobre el caso de trabajo propuesto:

> Caso sugerido: Sistema de Gestión de Solicitudes Académicas. El sistema permite registrar solicitudes de estudiantes, clasificarlas por tipo, prioridad y estado, asignar un responsable, consultar solicitudes y generar un reporte simple.

El sistema base es un prototipo de consola construido por el equipo para este trabajo. Se eligió un prototipo propio y acotado porque permite controlar el alcance y concentrar el esfuerzo en el diagnóstico, las decisiones de diseño y la evidencia técnica.

### Alcance y funcionalidades

| N° | Funcionalidad | Descripción |
|---|---|---|
| 1 | Registrar solicitud | Pide estudiante, correo, tipo, descripción y prioridad, y la guarda como Pendiente con un ID correlativo. |
| 2 | Listar solicitudes | Muestra todas las solicitudes con su ID, estudiante, tipo, prioridad, estado y responsable. |
| 3 | Cambiar estado | Pasa una solicitud a Pendiente, En proceso o Resuelta. |
| 4 | Asignar responsable | Registra el nombre y el área de quien atiende la solicitud. |
| 5 | Filtrar por estado | Muestra solo las solicitudes del estado indicado. |
| 6 | Reporte | Muestra el total de solicitudes y la cantidad en cada estado. |

Quedan fuera del alcance la interfaz gráfica, los usuarios con autenticación, la eliminación de solicitudes y el uso de una base de datos.

### Actores

| Actor | Participación |
|---|---|
| Personal administrativo | Es quien opera la consola: registra solicitudes, cambia su estado, asigna responsables y consulta listados, filtros y reportes. |
| Estudiante | Presenta la solicitud. Sus datos (nombre y correo) quedan registrados en ella. |
| Responsable o área | Atiende la solicitud asignada. Se registran su nombre y su área. |

### Estructuras principales

| Estructura | Contenido |
|---|---|
| Solicitud | ID, tipo, descripción, prioridad, estado, estudiante y responsable. |
| Estudiante | Nombre y correo, dentro de cada solicitud. |
| Responsable | Nombre y área, dentro de cada solicitud; vacío hasta que se asigna. |

En la versión inicial son diccionarios anidados que se guardan en `solicitudes.json`. El estado y la prioridad son textos.

### Tecnología

- Lenguaje: Python 3 (versión 3.9 o superior), sin librerías externas.
- Persistencia: archivo JSON (`solicitudes.json`).
- Pruebas: pytest.
- Análisis del código: Pylint, Flake8 y Radon.
- Control de versiones: Git y GitHub.

### Versión inicial y repositorio

La versión inicial es el archivo `main.py`, de 120 líneas, subido en el commit `57d495f` y marcada con el tag `estado-inicial` en https://github.com/GonzaloTozzi/TPI_MetodologiaII.

### Evidencia de funcionamiento

Ejecución real de la versión inicial. Se muestra el menú completo la primera vez y después solo las operaciones; los valores que siguen a cada pregunta son los ingresados por teclado.

```
=== SOLICITUDES ACADÉMICAS ===
1. Registrar solicitud
2. Listar solicitudes
3. Cambiar estado
4. Asignar responsable
5. Filtrar por estado
6. Reporte
0. Salir
Opción: 1
Estudiante: Ana Pérez
Correo: ana.perez@ejemplo.com
Tipo de solicitud: Certificado
Descripción: Certificado de alumno regular
Prioridad (Baja/Media/Alta): Alta
Registrada.
(menú)
Opción: 4
ID: 1
Responsable: Laura Gómez
Área: Alumnado
Asignado.
(menú)
Opción: 3
ID: 1
Estado (Pendiente/En proceso/Resuelta): en proceso
No se pudo actualizar.
(menú)
Opción: 2
#1 | Ana Pérez | Certificado | Alta | Pendiente | Responsable: {'nombre': 'Laura Gómez', 'area': 'Alumnado'}
(menú)
Opción: 5
Estado a filtrar: Resuelta
(menú)
Opción: 6
Total: 1
Pendiente: 1
En proceso: 0
Resuelta: 0
(menú)
Opción: 0
```

## Etapa 2: Calidad externa vs. calidad interna

### Calidad externa

Desde la mirada del usuario, el sistema cumple su función: el menú es claro, las seis operaciones funcionan con datos correctos y la información se conserva entre ejecuciones. Sin embargo, al probar casos menos frecuentes aparecen seis defectos visibles, cada uno documentado con una prueba en `tests/test_defectos_conocidos.py`.

| N° | Defecto visible | Ejemplo | Prueba |
|---|---|---|---|
| 1 | El listado muestra el responsable con la estructura interna del programa. | `Responsable: {'nombre': 'Laura Gómez', 'area': 'Alumnado'}` | `test_listado_muestra_el_responsable_como_diccionario` |
| 2 | Al cambiar el estado, "en proceso" en minúsculas se rechaza, aunque al filtrar "pendiente" en minúsculas sí funciona. | `Estado (Pendiente/En proceso/Resuelta): en proceso > No se pudo actualizar.` | `test_cambiar_estado_rechaza_el_estado_escrito_en_minusculas` |
| 3 | Errores distintos muestran el mismo mensaje: un ID inexistente y un estado inválido dan "No se pudo actualizar." | `ID: 99 > No se pudo actualizar.  /  Estado: Cerrada > No se pudo actualizar.` | `test_errores_distintos_muestran_el_mismo_mensaje` |
| 4 | La prioridad pide Baja, Media o Alta pero acepta cualquier texto, y el correo puede quedar vacío. | `Prioridad (Baja/Media/Alta): Urgentísima > Registrada.` | `test_registrar_acepta_prioridad_y_correo_sin_validar` |
| 5 | Si ninguna solicitud coincide con el filtro, el programa vuelve al menú sin avisar. | `Estado a filtrar: Resuelta > (no se muestra nada)` | `test_filtrar_sin_resultados_no_muestra_ningun_mensaje` |
| 6 | Si solicitudes.json está dañado, el programa se cierra con un error sin controlar. | `json.decoder.JSONDecodeError (el usuario ve el detalle técnico del error)` | `test_archivo_de_datos_corrupto_cierra_el_programa` |

### Calidad interna

Por dentro, el sistema está escrito en un solo archivo de 120 líneas con 10 funciones, donde conviven la lectura de teclado, el menú, las validaciones, las reglas de negocio, el formato de salida y el acceso al archivo JSON. La función `main()` tiene 41 líneas y complejidad ciclomática 14. Las operaciones de negocio guardan directamente en un archivo con ruta fija, los estados válidos están escritos a mano en varios lugares y los errores se informan devolviendo `False`, sin indicar la causa.

### Relación con la mantenibilidad, la legibilidad y la evolución futura

- **Agregar un estado "Rechazada":** obliga a modificar tres lugares (líneas 45, 72 y 98). Si se olvida uno, el sistema queda inconsistente: por ejemplo, el estado se acepta pero el reporte no lo cuenta.
- **Agregar un dato a la solicitud, como la carrera:** hay que cambiar la firma de `registrar()` (línea 19), su llamada (línea 89), el diccionario que se arma (líneas 23 a 25) y la línea del listado (línea 34).
- **Cambiar el archivo JSON por una base de datos:** obliga a modificar las operaciones de negocio que llaman a `guardar()` (líneas 26, 51 y 60), además de `cargar()` y `guardar()`.
- **Legibilidad:** la línea 34 tiene 158 caracteres, y para entender una sola opción del menú hay que leer toda la función `main()`.
- **Pruebas:** como las consultas imprimen en lugar de devolver datos, la única forma de probarlas es ejecutar el programa completo y leer la consola.

Esa diferencia entre una calidad externa aceptable y una calidad interna baja es la deuda técnica que se diagnostica en la etapa 3.

## Etapa 3: Deuda técnica y code smells

Se identificaron 12 code smells y debilidades técnicas en la versión inicial. Para cada uno se indican la evidencia, la ubicación, el impacto, el riesgo de mantenimiento y la prioridad de corrección.

### Resumen

| N° | Code smell | Ubicación | Prioridad |
|---|---|---|---|
| 1 | Long Method | main.py, función main(), líneas 76 a 116. | Alta |
| 2 | Duplicated Code | main.py, función main(), líneas 93 a 97 y 101 a 105. | Media |
| 3 | Long Parameter List | main.py, función registrar(), línea 19; llamada en la línea 89. | Alta |
| 4 | Data Clumps | main.py, líneas 19 y 23 (estudiante y correo) y líneas 55 y 59 (nombre y área del responsable). | Media |
| 5 | Magic Strings / Primitive Obsession | main.py, líneas 25, 45, 72 y 98. | Alta |
| 6 | Feature Envy | main.py, funciones listar() (línea 34) y filtrar() (línea 67). | Media |
| 7 | Lógica mezclada con presentación (SRP) | main.py, funciones listar() (líneas 30 a 34), filtrar() (64 a 67) y reporte() (70 a 73). | Media |
| 8 | Módulo con demasiadas responsabilidades (God Module) | main.py completo: 120 líneas y 10 funciones. | Alta |
| 9 | Acoplamiento directo a la persistencia (DIP) | main.py, línea 4 (ARCHIVO) y llamadas a guardar() en las líneas 26, 51 y 60. | Alta |
| 10 | Manejo de errores por valores de retorno y validación incompleta | main.py, líneas 21, 46, 49 y 58 (return False), función cargar() (líneas 7 a 11) y validación de registrar() (línea 20). | Alta |
| 11 | Switch Statements (OCP) | main.py, función main(), líneas 83 a 116, y texto del menú en las líneas 80 y 81. | Media |
| 12 | Nombres poco expresivos | main.py, variable s (líneas 22, 33, 38, 65 y 73) y funciones asignar() (línea 55) y filtrar() (línea 64). | Baja |

### Métricas de la versión inicial

| Indicador | Valor |
|---|---|
| Archivos de código | 1 |
| Líneas de código (SLOC) | 97 |
| Complejidad ciclomática máxima (Radon) | 14, main() (C) |
| Complejidad ciclomática promedio (Radon) | 4,1 |
| Funciones con más de 5 parámetros | 1, registrar() |
| Pylint, todas las reglas | 8,19/10 con 17 observaciones |
| Flake8 (línea máxima 100, complejidad máxima 10) | 6 observaciones |
| Pruebas automatizadas | 28 |

La salida completa de las herramientas está en `docs/evidencias/metricas_estado_inicial.txt`.

### Smell 1. Long Method

**Ubicación:** main.py, función main(), líneas 76 a 116.

**Evidencia:**

```python
        opcion = input("Opción: ").strip()
        if opcion == "1":
            estudiante = input("Estudiante: ")
            correo = input("Correo: ")
            tipo = input("Tipo de solicitud: ")
            descripcion = input("Descripción: ")
            prioridad = input("Prioridad (Baja/Media/Alta): ")
            print("Registrada." if registrar(solicitudes, estudiante, correo, tipo,
                  descripcion, prioridad) else "Datos inválidos.")
        elif opcion == "2":
```

Radon: complejidad ciclomática 14 (categoría C). Flake8: C901 'main' is too complex.

**Impacto:** La función mezcla el menú, la lectura de cada dato, la conversión del ID, la llamada a cada operación y el mensaje al usuario. Para entender o cambiar una sola opción hay que leer las 41 líneas.

**Riesgo de mantenimiento:** Alto. Cada opción nueva se agrega dentro de la misma función y aumenta su complejidad; un cambio en una rama puede afectar a otra sin que se note.

**Prioridad de corrección:** Alta

**Corrección propuesta:** Extract Method: una función por opción del menú y una función para leer el ID.

### Smell 2. Duplicated Code

**Ubicación:** main.py, función main(), líneas 93 a 97 y 101 a 105.

**Evidencia:**

```python
            try:
                identificador = int(input("ID: "))
            except ValueError:
                print("ID inválido.")
                continue
```

El mismo bloque aparece en las opciones 3 (cambiar estado) y 4 (asignar responsable).

**Impacto:** La lectura y la validación del ID están escritas dos veces.

**Riesgo de mantenimiento:** Medio. Si cambia la validación o el mensaje, hay que corregir los dos lugares; si se corrige uno solo, el sistema responde distinto según la opción.

**Prioridad de corrección:** Media

**Corrección propuesta:** Extract Method: una única función leer_id().

### Smell 3. Long Parameter List

**Ubicación:** main.py, función registrar(), línea 19; llamada en la línea 89.

**Evidencia:**

```python
def registrar(solicitudes, estudiante, correo, tipo, descripcion, prioridad):
```

Pylint: R0913 too-many-arguments (6/5) y R0917 too-many-positional-arguments (6/5).

**Impacto:** Seis parámetros posicionales, cinco de ellos textos, se pueden pasar en un orden equivocado sin que Python lo detecte.

**Riesgo de mantenimiento:** Alto. Agregar un dato a la solicitud (por ejemplo, la carrera) obliga a cambiar la firma, la llamada y el diccionario que se arma adentro.

**Prioridad de corrección:** Alta

**Corrección propuesta:** Introduce Parameter Object: agrupar los datos de entrada en un objeto DatosSolicitud.

### Smell 4. Data Clumps

**Ubicación:** main.py, líneas 19 y 23 (estudiante y correo) y líneas 55 y 59 (nombre y área del responsable).

**Evidencia:**

```python
def asignar(solicitudes, identificador, nombre, area):
    ...
    solicitud["responsable"] = {"nombre": nombre, "area": area}
```

**Impacto:** Los datos que forman al estudiante y al responsable viajan siempre juntos pero sueltos, sin una estructura que los represente.

**Riesgo de mantenimiento:** Medio. Las reglas de esos datos, como el formato del correo, no tienen un lugar propio y terminarían repetidas en distintas funciones.

**Prioridad de corrección:** Media

**Corrección propuesta:** Introduce Parameter Object: clases Estudiante y Responsable.

### Smell 5. Magic Strings / Primitive Obsession

**Ubicación:** main.py, líneas 25, 45, 72 y 98.

**Evidencia:**

```python
    if estado not in ("Pendiente", "En proceso", "Resuelta"):
    ...
    for estado in ("Pendiente", "En proceso", "Resuelta"):
```

Líneas 45 y 72. Los mismos textos aparecen también en la línea 25 (estado inicial) y en la 98 (mensaje del menú).

**Impacto:** Los estados válidos están escritos a mano en cuatro lugares y la prioridad es texto libre. Además, cambiar_estado() compara el texto exacto mientras que filtrar() ignora mayúsculas, y por eso se comportan distinto.

**Riesgo de mantenimiento:** Alto. Agregar o renombrar un estado obliga a modificar tres lugares (líneas 45, 72 y 98), y un error de tipeo en cualquiera de ellos no se detecta hasta ejecutar.

**Prioridad de corrección:** Alta

**Corrección propuesta:** Reemplazar los literales por las enumeraciones Estado y Prioridad, con una única regla de comparación.

### Smell 6. Feature Envy

**Ubicación:** main.py, funciones listar() (línea 34) y filtrar() (línea 67).

**Evidencia:**

```python
print(f'#{s["id"]} | {s["estudiante"]["nombre"]} | {s["tipo"]} | {s["prioridad"]} | '
      f'{s["estado"]} | Responsable: {s["responsable"] or "Sin asignar"}')
...
print(f'#{s["id"]}: {s["descripcion"]} ({s["estado"]})')
```

La línea 34 original ocupa 158 caracteres; se muestra partida para que sea legible.

**Impacto:** Las funciones de listado arman el texto de una solicitud metiéndose en la estructura interna del diccionario. Cada una lo hace con un formato distinto, y el listado termina imprimiendo el responsable como diccionario.

**Riesgo de mantenimiento:** Medio. Cambiar la estructura de la solicitud obliga a revisar todas las funciones que la recorren.

**Prioridad de corrección:** Media

**Corrección propuesta:** Move Method: llevar el formato de la solicitud a la clase Solicitud.

### Smell 7. Lógica mezclada con presentación (SRP)

**Ubicación:** main.py, funciones listar() (líneas 30 a 34), filtrar() (64 a 67) y reporte() (70 a 73).

**Evidencia:**

```python
def reporte(solicitudes):
    print(f"Total: {len(solicitudes)}")
    for estado in ("Pendiente", "En proceso", "Resuelta"):
        print(f'{estado}: {sum(1 for s in solicitudes if s["estado"] == estado)}')
```

**Impacto:** Las consultas imprimen el resultado en lugar de devolverlo, así que no se pueden reutilizar (por ejemplo, para exportar o mostrar en otra interfaz) ni probar sin capturar la consola.

**Riesgo de mantenimiento:** Medio. Cualquier cambio de interfaz obliga a reescribir también el cálculo.

**Prioridad de corrección:** Media

**Corrección propuesta:** Separar la consulta, que devuelve datos, de la presentación en consola.

### Smell 8. Módulo con demasiadas responsabilidades (God Module)

**Ubicación:** main.py completo: 120 líneas y 10 funciones.

**Evidencia:**

```python
cargar(), guardar()                  > acceso al archivo
registrar(), cambiar_estado(),
asignar(), buscar_por_id()            > validaciones y reglas de negocio
listar(), filtrar(), reporte()        > formato y salida por pantalla
main()                                > menú y lectura de teclado
```

Todas estas funciones están en el mismo archivo.

**Impacto:** No hay límites entre componentes: cualquier cambio, sea de interfaz, de reglas o de almacenamiento, se hace sobre el mismo archivo.

**Riesgo de mantenimiento:** Alto. A medida que el sistema crezca, el archivo acumula más motivos de cambio y aumenta la probabilidad de regresiones.

**Prioridad de corrección:** Alta

**Corrección propuesta:** Extract Class y Move Method: separar en modelos, repositorio, servicio y consola.

### Smell 9. Acoplamiento directo a la persistencia (DIP)

**Ubicación:** main.py, línea 4 (ARCHIVO) y llamadas a guardar() en las líneas 26, 51 y 60.

**Evidencia:**

```python
ARCHIVO = "solicitudes.json"
...
    solicitud["estado"] = estado
    guardar(solicitudes)
    return True
```

**Impacto:** Las operaciones de negocio dependen de una función concreta que escribe un archivo JSON con una ruta fija.

**Riesgo de mantenimiento:** Alto. Cambiar el almacenamiento (por ejemplo, a SQLite) obliga a modificar las operaciones de negocio, y no se las puede probar sin escribir en un archivo.

**Prioridad de corrección:** Alta

**Corrección propuesta:** Introducir un repositorio detrás de una abstracción y pasarlo al servicio desde afuera.

### Smell 10. Manejo de errores por valores de retorno y validación incompleta

**Ubicación:** main.py, líneas 21, 46, 49 y 58 (return False), función cargar() (líneas 7 a 11) y validación de registrar() (línea 20).

**Evidencia:**

```python
    if estado not in ("Pendiente", "En proceso", "Resuelta"):
        return False
    solicitud = buscar_por_id(solicitudes, identificador)
    if solicitud is None:
        return False
```

**Impacto:** Errores distintos devuelven el mismo False y el usuario ve el mismo mensaje. Se validan nombre y descripción, pero no el correo, el tipo ni la prioridad. Un solicitudes.json dañado cierra el programa con un error sin controlar.

**Riesgo de mantenimiento:** Alto. Se guardan datos inconsistentes y los errores son difíciles de diagnosticar.

**Prioridad de corrección:** Alta

**Corrección propuesta:** Replace Error Code with Exception, con mensajes que indiquen la causa, y validación completa al registrar.

### Smell 11. Switch Statements (OCP)

**Ubicación:** main.py, función main(), líneas 83 a 116, y texto del menú en las líneas 80 y 81.

**Evidencia:**

```python
        if opcion == "1":
            ...
        elif opcion == "2":
            listar(solicitudes)
        ...
        elif opcion == "0":
            break
        else:
            print("Opción inválida.")
```

**Impacto:** Agregar una opción al menú obliga a modificar la cadena de condiciones y, por separado, el texto del menú.

**Riesgo de mantenimiento:** Medio. Es fácil que el texto del menú y las opciones que realmente existen queden desalineados.

**Prioridad de corrección:** Media

**Corrección propuesta:** Reemplazar la cadena de condiciones por una tabla de opciones que también genere el texto del menú.

### Smell 12. Nombres poco expresivos

**Ubicación:** main.py, variable s (líneas 22, 33, 38, 65 y 73) y funciones asignar() (línea 55) y filtrar() (línea 64).

**Evidencia:**

```python
    for s in solicitudes:
...
def asignar(solicitudes, identificador, nombre, area):
```

**Impacto:** s no dice qué contiene; asignar no dice qué se asigna; filtrar imprime, aunque el nombre sugiere que devuelve el resultado.

**Riesgo de mantenimiento:** Bajo. Dificulta la lectura pero no provoca fallas por sí solo.

**Prioridad de corrección:** Baja

**Corrección propuesta:** Renombrar: solicitud, asignar_responsable, filtrar_por_estado.
