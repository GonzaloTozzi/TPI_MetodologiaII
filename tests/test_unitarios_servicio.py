"""Pruebas unitarias del servicio usando un repositorio en memoria.

El servicio depende de la abstracción RepositorioSolicitudes y no del archivo
JSON, así que se puede probar con cualquier implementación que la respete.
"""

import pytest

from errores import DatosInvalidos, SolicitudNoEncontrada
from modelos import DatosSolicitud, Estado, Estudiante, Responsable, Solicitud
from servicio import ServicioSolicitudes


class RepositorioEnMemoria:
    def __init__(self, solicitudes=None):
        self.guardadas = list(solicitudes or [])
        self.veces_guardado = 0

    def cargar_todas(self):
        return list(self.guardadas)

    def guardar_todas(self, solicitudes):
        self.guardadas = list(solicitudes)
        self.veces_guardado += 1


def datos(nombre="Ana Pérez", descripcion="Certificado de alumno regular"):
    return DatosSolicitud(
        estudiante=Estudiante(nombre, "alumno@ejemplo.com"),
        tipo="Certificado",
        descripcion=descripcion,
        prioridad="Alta",
    )


@pytest.fixture
def repositorio():
    return RepositorioEnMemoria()


@pytest.fixture
def servicio(repositorio):
    return ServicioSolicitudes(repositorio)


def test_carga_las_solicitudes_que_ya_tiene_el_repositorio():
    existente = Solicitud.nueva(5, datos())
    servicio = ServicioSolicitudes(RepositorioEnMemoria([existente]))

    assert servicio.listar() == [existente]
    assert servicio.registrar(datos("Bruno Díaz")).id == 6


def test_registrar_asigna_ids_correlativos_y_guarda(servicio, repositorio):
    primera = servicio.registrar(datos("Ana Pérez"))
    segunda = servicio.registrar(datos("Bruno Díaz"))

    assert (primera.id, segunda.id) == (1, 2)
    assert repositorio.veces_guardado == 2
    assert len(repositorio.guardadas) == 2


def test_registrar_con_datos_invalidos_no_guarda(servicio, repositorio):
    with pytest.raises(DatosInvalidos):
        servicio.registrar(datos(descripcion=""))

    assert repositorio.veces_guardado == 0


def test_cambiar_estado_guarda_el_cambio(servicio, repositorio):
    servicio.registrar(datos())

    servicio.cambiar_estado(1, "resuelta")

    assert repositorio.veces_guardado == 2
    assert repositorio.guardadas[0].estado is Estado.RESUELTA


def test_cambiar_estado_de_id_inexistente_no_guarda(servicio, repositorio):
    with pytest.raises(SolicitudNoEncontrada, match="ID 99"):
        servicio.cambiar_estado(99, "Resuelta")

    assert repositorio.veces_guardado == 0


def test_asignar_responsable_sin_nombre_no_guarda(servicio, repositorio):
    servicio.registrar(datos())

    with pytest.raises(DatosInvalidos, match="responsable es obligatorio"):
        servicio.asignar_responsable(1, Responsable("  ", "Alumnado"))

    assert repositorio.veces_guardado == 1
    assert repositorio.guardadas[0].responsable is None


def test_filtrar_y_contar_por_estado(servicio):
    servicio.registrar(datos("Ana Pérez"))
    servicio.registrar(datos("Bruno Díaz"))
    servicio.cambiar_estado(2, "En proceso")

    assert [s.id for s in servicio.filtrar_por_estado("en proceso")] == [2]
    assert servicio.contar_por_estado() == {
        Estado.PENDIENTE: 1,
        Estado.EN_PROCESO: 1,
        Estado.RESUELTA: 0,
    }
