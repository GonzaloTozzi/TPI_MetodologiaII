"""Pruebas unitarias del modelo, sin pasar por la consola ni por el archivo."""

import pytest

from errores import DatosInvalidos
from modelos import (
    DatosSolicitud,
    Estado,
    Estudiante,
    Prioridad,
    Responsable,
    Solicitud,
    correo_valido,
)


def datos_validos(**cambios):
    valores = {
        "estudiante": Estudiante("Ana Pérez", "ana.perez@ejemplo.com"),
        "tipo": "Certificado",
        "descripcion": "Certificado de alumno regular",
        "prioridad": "Alta",
    }
    valores.update(cambios)
    return DatosSolicitud(**valores)


def test_estado_desde_texto_ignora_mayusculas_y_espacios():
    assert Estado.desde_texto("  en PROCESO ") is Estado.EN_PROCESO


def test_estado_desde_texto_invalido_informa_las_opciones():
    with pytest.raises(DatosInvalidos, match="Pendiente, En proceso o Resuelta"):
        Estado.desde_texto("Cerrada")


def test_prioridad_desde_texto():
    assert Prioridad.desde_texto("media") is Prioridad.MEDIA


@pytest.mark.parametrize(
    "correo, esperado",
    [
        ("ana.perez@ejemplo.com", True),
        ("", False),
        ("ana.perez", False),
        ("@ejemplo.com", False),
        ("ana perez@ejemplo.com", False),
    ],
)
def test_correo_valido(correo, esperado):
    assert correo_valido(correo) is esperado


def test_solicitud_nueva_empieza_pendiente_y_normaliza_la_prioridad():
    solicitud = Solicitud.nueva(1, datos_validos(prioridad="alta"))

    assert solicitud.estado is Estado.PENDIENTE
    assert solicitud.prioridad == "Alta"
    assert solicitud.responsable is None


def test_solicitud_nueva_rechaza_descripcion_vacia():
    with pytest.raises(DatosInvalidos, match="descripción es obligatoria"):
        Solicitud.nueva(1, datos_validos(descripcion="   "))


def test_responsable_se_muestra_con_y_sin_area():
    assert str(Responsable("Laura Gómez", "Alumnado")) == "Laura Gómez (Alumnado)"
    assert str(Responsable("Laura Gómez", "")) == "Laura Gómez"


def test_solicitud_se_convierte_a_diccionario_y_vuelve_igual():
    solicitud = Solicitud.nueva(1, datos_validos())
    solicitud.asignar_responsable(Responsable("Laura Gómez", "Alumnado"))
    solicitud.cambiar_estado(Estado.RESUELTA)

    assert Solicitud.desde_dict(solicitud.a_dict()) == solicitud
