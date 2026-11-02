"""Defectos visibles de la versión inicial.

Estos tests documentan cómo funciona hoy el sistema base en situaciones donde
el comportamiento es mejorable. Si el refactoring corrige alguno de estos
puntos, el test correspondiente va a fallar: en ese caso se actualiza para
reflejar el nuevo comportamiento y el cambio se registra como mejora.
"""

from datos_prueba import ANA, LISTAR, asignacion, cambio_estado, filtro, registro


def test_cambiar_estado_rechaza_el_estado_escrito_en_minusculas(app):
    """Filtrar acepta "pendiente", pero cambiar estado rechaza "en proceso"."""
    resultado = app.ejecutar(*ANA, *cambio_estado("1", "en proceso"), *LISTAR)

    assert "No se pudo actualizar." in resultado.stdout
    assert "#1 | Ana Pérez | Certificado | Alta | Pendiente |" in resultado.stdout


def test_errores_distintos_muestran_el_mismo_mensaje(app):
    """El usuario no puede saber si falló el ID o el dato que ingresó."""
    resultado = app.ejecutar(
        *ANA,
        *cambio_estado("99", "Resuelta"),
        *cambio_estado("1", "Cerrada"),
        *asignacion("99", "Laura Gómez", "Alumnado"),
        *asignacion("1", "   ", "Alumnado"),
    )

    assert resultado.stdout.count("No se pudo actualizar.") == 2
    assert resultado.stdout.count("No se pudo asignar.") == 2


def test_registrar_acepta_prioridad_y_correo_sin_validar(app):
    """La prioridad pide Baja/Media/Alta pero acepta cualquier texto, y el correo puede quedar vacío."""
    entradas = registro("Darío Sosa", "", "Consulta", "Consulta general", "Urgentísima")
    resultado = app.ejecutar(*entradas, *LISTAR)

    assert "Registrada." in resultado.stdout
    assert "#1 | Darío Sosa | Consulta | Urgentísima | Pendiente |" in resultado.stdout


def test_listado_muestra_el_responsable_como_diccionario(app):
    """El listado imprime la estructura interna en lugar de un texto legible."""
    resultado = app.ejecutar(*ANA, *asignacion("1", "Laura Gómez", "Alumnado"), *LISTAR)

    assert "Responsable: {'nombre': 'Laura Gómez', 'area': 'Alumnado'}" in resultado.stdout


def test_filtrar_sin_resultados_no_muestra_ningun_mensaje(app):
    """Si ninguna solicitud coincide, el programa vuelve al menú sin avisar."""
    resultado = app.ejecutar(*ANA, *filtro("Resuelta"))

    despues_del_filtro = resultado.stdout.split("Estado a filtrar: ", 1)[1]
    lineas = [linea for linea in despues_del_filtro.splitlines() if linea.strip()]

    # Lo primero que aparece es el encabezado del menú y enseguida sus opciones.
    assert lineas[1].startswith("1. Registrar solicitud")


def test_archivo_de_datos_corrupto_cierra_el_programa(app):
    """Si solicitudes.json está dañado, el programa termina con un error sin controlar."""
    app.archivo_datos.write_text("{esto no es json", encoding="utf-8")

    resultado = app.ejecutar(*LISTAR)

    assert resultado.returncode != 0
    assert "JSONDecodeError" in resultado.stderr
