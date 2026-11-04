"""Casos de uso del sistema de solicitudes."""

from __future__ import annotations

from errores import SolicitudNoEncontrada
from modelos import DatosSolicitud, Estado, Responsable, Solicitud
from repositorio import RepositorioSolicitudes


class ServicioSolicitudes:
    """Reglas de negocio; no conoce la consola ni el formato del archivo."""

    def __init__(self, repositorio: RepositorioSolicitudes) -> None:
        self._repositorio = repositorio
        self._solicitudes = repositorio.cargar_todas()

    def listar(self) -> list[Solicitud]:
        """Devuelve todas las solicitudes."""
        return list(self._solicitudes)

    def registrar(self, datos: DatosSolicitud) -> Solicitud:
        """Registra una solicitud nueva con el siguiente ID disponible."""
        solicitud = Solicitud.nueva(self._siguiente_id(), datos)
        self._solicitudes.append(solicitud)
        self._guardar()
        return solicitud

    def cambiar_estado(self, identificador: int, texto_estado: str) -> Solicitud:
        """Cambia el estado de la solicitud indicada."""
        estado = Estado.desde_texto(texto_estado)
        solicitud = self._buscar(identificador)
        solicitud.cambiar_estado(estado)
        self._guardar()
        return solicitud

    def asignar_responsable(self, identificador: int, responsable: Responsable) -> Solicitud:
        """Asigna un responsable a la solicitud indicada."""
        solicitud = self._buscar(identificador)
        solicitud.asignar_responsable(responsable)
        self._guardar()
        return solicitud

    def filtrar_por_estado(self, texto_estado: str) -> list[Solicitud]:
        """Devuelve las solicitudes del estado indicado, sin distinguir mayúsculas."""
        buscado = texto_estado.lower()
        return [s for s in self._solicitudes if s.estado.value.lower() == buscado]

    def contar_por_estado(self) -> dict[Estado, int]:
        """Cantidad de solicitudes en cada estado, para el reporte."""
        return {
            estado: sum(1 for s in self._solicitudes if s.estado is estado)
            for estado in Estado
        }

    def _buscar(self, identificador: int) -> Solicitud:
        for solicitud in self._solicitudes:
            if solicitud.id == identificador:
                return solicitud
        raise SolicitudNoEncontrada(identificador)

    def _siguiente_id(self) -> int:
        return max((s.id for s in self._solicitudes), default=0) + 1

    def _guardar(self) -> None:
        self._repositorio.guardar_todas(self._solicitudes)
