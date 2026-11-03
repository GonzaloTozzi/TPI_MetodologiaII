"""Defectos visibles de la versión inicial, ya corregidos.

Cada test reemplaza al que documentaba el defecto en la versión inicial y
verifica el nuevo comportamiento.
"""

from datos_prueba import ANA, LISTAR, asignacion, cambio_estado, filtro, registro


def test_cambiar_estado_acepta_el_estado_escrito_en_minusculas(app):
    """Antes se rechazaba "en proceso" aunque filtrar sí aceptaba minúsculas."""
    resultado = app.ejecutar(*ANA, *cambio_estado("1", "en proceso"), *LISTAR)

    assert "Actualizado." in resultado.stdout
    assert "#1 | Ana Pérez | Certificado | Alta | En proceso |" in resultado.stdout


def test_errores_distintos_muestran_mensajes_distintos(app):
    """Antes un ID inexistente y un dato inválido mostraban el mismo mensaje."""
    resultado = app.ejecutar(
        *ANA,
        *cambio_estado("99", "Resuelta"),
        *cambio_estado("1", "Cerrada"),
        *asignacion("99", "Laura Gómez", "Alumnado"),
        *asignacion("1", "   ", "Alumnado"),
    )

    assert "No se pudo actualizar: no existe una solicitud con ID 99." in resultado.stdout
    assert (
        "No se pudo actualizar: el estado debe ser Pendiente, En proceso o Resuelta."
        in resultado.stdout
    )
    assert "No se pudo asignar: no existe una solicitud con ID 99." in resultado.stdout
    assert (
        "No se pudo asignar: el nombre del responsable es obligatorio." in resultado.stdout
    )


def test_registrar_valida_prioridad_y_correo(app):
    """Antes se aceptaba cualquier prioridad y el correo podía quedar vacío."""
    prioridad_invalida = registro(
        "Darío Sosa", "dario.sosa@ejemplo.com", "Consulta", "Consulta general", "Urgentísima"
    )
    correo_vacio = registro("Darío Sosa", "", "Consulta", "Consulta general", "Alta")
    resultado = app.ejecutar(*prioridad_invalida, *correo_vacio, *LISTAR)

    assert "Datos inválidos: la prioridad debe ser Baja, Media o Alta." in resultado.stdout
    assert "Datos inválidos: el correo no es válido." in resultado.stdout
    assert "No hay solicitudes." in resultado.stdout


def test_registrar_normaliza_la_prioridad(app):
    """La prioridad escrita en minúsculas se guarda con el formato de las opciones."""
    entradas = registro(
        "Darío Sosa", "dario.sosa@ejemplo.com", "Consulta", "Consulta general", "alta"
    )
    resultado = app.ejecutar(*entradas, *LISTAR)

    assert "#1 | Darío Sosa | Consulta | Alta | Pendiente |" in resultado.stdout


def test_listado_muestra_el_responsable_en_texto_legible(app):
    """Antes el listado mostraba la estructura interna del responsable."""
    resultado = app.ejecutar(*ANA, *asignacion("1", "Laura Gómez", "Alumnado"), *LISTAR)

    assert "Responsable: Laura Gómez (Alumnado)" in resultado.stdout
    assert "{'nombre'" not in resultado.stdout


def test_filtrar_sin_resultados_avisa(app):
    """Antes el programa volvía al menú sin mostrar ningún mensaje."""
    resultado = app.ejecutar(*ANA, *filtro("Resuelta"))

    assert "No hay solicitudes con ese estado." in resultado.stdout


def test_archivo_de_datos_danado_muestra_un_mensaje_y_no_se_pierde(app):
    """Antes el programa terminaba con un error sin controlar."""
    contenido = "{esto no es json"
    app.archivo_datos.write_text(contenido, encoding="utf-8")

    resultado = app.ejecutar(*LISTAR)

    assert resultado.returncode == 1
    assert "Traceback" not in resultado.stderr
    assert "No se pudo leer el archivo solicitudes.json" in resultado.stderr
    assert app.archivo_datos.read_text(encoding="utf-8") == contenido
