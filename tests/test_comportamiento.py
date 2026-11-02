"""Comportamiento externo del sistema.

Estos tests tienen que pasar igual antes y después del refactoring. Si alguno
falla después de un cambio, el refactoring alteró lo que ve el usuario.
"""

from datos_prueba import (
    ANA,
    BRUNO,
    CARLA,
    LISTAR,
    REPORTE,
    asignacion,
    cambio_estado,
    filtro,
    registro,
)


def test_salir_con_opcion_cero_termina_sin_error(app):
    resultado = app.ejecutar()

    assert resultado.returncode == 0


def test_opcion_inexistente_muestra_mensaje(app):
    resultado = app.ejecutar("9")

    assert "Opción inválida." in resultado.stdout


def test_listar_sin_solicitudes(app):
    resultado = app.ejecutar(*LISTAR)

    assert "No hay solicitudes." in resultado.stdout


def test_registrar_solicitud_valida(app):
    resultado = app.ejecutar(*ANA, *LISTAR)

    assert "Registrada." in resultado.stdout
    assert (
        "#1 | Ana Pérez | Certificado | Alta | Pendiente | Responsable: Sin asignar"
        in resultado.stdout
    )


def test_registrar_asigna_ids_correlativos(app):
    resultado = app.ejecutar(*ANA, *BRUNO, *LISTAR)

    assert "#1 | Ana Pérez" in resultado.stdout
    assert "#2 | Bruno Díaz" in resultado.stdout


def test_registrar_rechaza_estudiante_vacio(app):
    entradas = registro("   ", "x@ejemplo.com", "Certificado", "Constancia", "Alta")
    resultado = app.ejecutar(*entradas, *LISTAR)

    assert "Registrada." not in resultado.stdout
    assert "No hay solicitudes." in resultado.stdout


def test_registrar_rechaza_descripcion_vacia(app):
    entradas = registro("Ana Pérez", "ana.perez@ejemplo.com", "Certificado", "  ", "Alta")
    resultado = app.ejecutar(*entradas, *LISTAR)

    assert "Registrada." not in resultado.stdout
    assert "No hay solicitudes." in resultado.stdout


def test_cambiar_estado_valido(app):
    resultado = app.ejecutar(*ANA, *cambio_estado("1", "En proceso"), *LISTAR)

    assert "Actualizado." in resultado.stdout
    assert "#1 | Ana Pérez | Certificado | Alta | En proceso |" in resultado.stdout


def test_cambiar_estado_invalido_no_modifica_la_solicitud(app):
    resultado = app.ejecutar(*ANA, *cambio_estado("1", "Cerrada"), *LISTAR)

    assert "Actualizado." not in resultado.stdout
    assert "#1 | Ana Pérez | Certificado | Alta | Pendiente |" in resultado.stdout


def test_cambiar_estado_de_id_inexistente_no_modifica_nada(app):
    resultado = app.ejecutar(*ANA, *cambio_estado("99", "Resuelta"), *LISTAR)

    assert "Actualizado." not in resultado.stdout
    assert "#1 | Ana Pérez | Certificado | Alta | Pendiente |" in resultado.stdout


def test_id_no_numerico_avisa_y_el_programa_sigue(app):
    resultado = app.ejecutar(*ANA, "3", "abc", "4", "xyz", *LISTAR)

    assert resultado.stdout.count("ID inválido.") == 2
    assert "#1 | Ana Pérez" in resultado.stdout
    assert resultado.returncode == 0


def test_asignar_responsable_valido(app):
    resultado = app.ejecutar(*ANA, *asignacion("1", "Laura Gómez", "Alumnado"), *LISTAR)

    assert "Asignado." in resultado.stdout
    assert "Laura Gómez" in resultado.stdout
    assert "Sin asignar" not in resultado.stdout


def test_asignar_rechaza_nombre_vacio(app):
    resultado = app.ejecutar(*ANA, *asignacion("1", "   ", "Alumnado"), *LISTAR)

    assert "Asignado." not in resultado.stdout
    assert "Responsable: Sin asignar" in resultado.stdout


def test_asignar_a_id_inexistente_no_modifica_nada(app):
    resultado = app.ejecutar(*ANA, *asignacion("99", "Laura Gómez", "Alumnado"), *LISTAR)

    assert "Asignado." not in resultado.stdout
    assert "Responsable: Sin asignar" in resultado.stdout


def test_filtrar_por_estado(app):
    resultado = app.ejecutar(*ANA, *BRUNO, *cambio_estado("2", "Resuelta"), *filtro("Resuelta"))

    assert "#2: Equivalencia de Programación I (Resuelta)" in resultado.stdout
    assert "#1:" not in resultado.stdout


def test_filtrar_no_distingue_mayusculas(app):
    resultado = app.ejecutar(*ANA, *filtro("pendiente"))

    assert "#1: Certificado de alumno regular (Pendiente)" in resultado.stdout


def test_reporte_cuenta_por_estado(app):
    resultado = app.ejecutar(
        *ANA,
        *BRUNO,
        *CARLA,
        *cambio_estado("2", "En proceso"),
        *cambio_estado("3", "Resuelta"),
        *REPORTE,
    )

    assert "Total: 3" in resultado.stdout
    assert "Pendiente: 1" in resultado.stdout
    assert "En proceso: 1" in resultado.stdout
    assert "Resuelta: 1" in resultado.stdout


def test_reporte_sin_solicitudes(app):
    resultado = app.ejecutar(*REPORTE)

    assert "Total: 0" in resultado.stdout
    assert "Pendiente: 0" in resultado.stdout
    assert "En proceso: 0" in resultado.stdout
    assert "Resuelta: 0" in resultado.stdout


def test_el_registro_persiste_entre_ejecuciones(app):
    app.ejecutar(*ANA)
    resultado = app.ejecutar(*LISTAR)

    assert "#1 | Ana Pérez | Certificado | Alta | Pendiente |" in resultado.stdout


def test_el_cambio_de_estado_persiste_entre_ejecuciones(app):
    app.ejecutar(*ANA)
    app.ejecutar(*cambio_estado("1", "En proceso"))
    resultado = app.ejecutar(*LISTAR)

    assert "#1 | Ana Pérez | Certificado | Alta | En proceso |" in resultado.stdout


def test_la_asignacion_persiste_entre_ejecuciones(app):
    app.ejecutar(*ANA)
    app.ejecutar(*asignacion("1", "Laura Gómez", "Alumnado"))
    resultado = app.ejecutar(*LISTAR)

    assert "Laura Gómez" in resultado.stdout


def test_archivo_de_datos_se_crea_al_registrar_la_primera_solicitud(app):
    app.ejecutar(*LISTAR)
    assert not app.archivo_datos.exists()

    app.ejecutar(*ANA)
    assert app.archivo_datos.exists()
