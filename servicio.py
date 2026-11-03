from __future__ import annotations

from typing import Optional

from modelos import DatosSolicitud, Estado, Responsable, Solicitud
from repositorio import RepositorioSolicitudes


class ServicioSolicitudes:
    def __init__(self, repositorio: RepositorioSolicitudes) -> None:
        self._repositorio = repositorio
        self._solicitudes = repositorio.cargar_todas()

    def listar(self) -> list[Solicitud]:
        return list(self._solicitudes)

    def registrar(self, datos: DatosSolicitud) -> bool:
        if not datos.estudiante.nombre.strip() or not datos.descripcion.strip():
            return False
        self._solicitudes.append(Solicitud(
            id=self._siguiente_id(),
            estudiante=datos.estudiante,
            tipo=datos.tipo,
            descripcion=datos.descripcion,
            prioridad=datos.prioridad,
        ))
        self._guardar()
        return True

    def cambiar_estado(self, identificador: int, texto_estado: str) -> bool:
        if texto_estado not in Estado.valores():
            return False
        solicitud = self._buscar(identificador)
        if solicitud is None:
            return False
        solicitud.cambiar_estado(Estado(texto_estado))
        self._guardar()
        return True

    def asignar_responsable(self, identificador: int, responsable: Responsable) -> bool:
        solicitud = self._buscar(identificador)
        if solicitud is None or not responsable.nombre.strip():
            return False
        solicitud.asignar_responsable(responsable)
        self._guardar()
        return True

    def filtrar_por_estado(self, texto_estado: str) -> list[Solicitud]:
        buscado = texto_estado.lower()
        return [s for s in self._solicitudes if s.estado.value.lower() == buscado]

    def contar_por_estado(self) -> dict[Estado, int]:
        return {
            estado: sum(1 for s in self._solicitudes if s.estado is estado)
            for estado in Estado
        }

    def _buscar(self, identificador: int) -> Optional[Solicitud]:
        for solicitud in self._solicitudes:
            if solicitud.id == identificador:
                return solicitud
        return None

    def _siguiente_id(self) -> int:
        return max((s.id for s in self._solicitudes), default=0) + 1

    def _guardar(self) -> None:
        self._repositorio.guardar_todas(self._solicitudes)
