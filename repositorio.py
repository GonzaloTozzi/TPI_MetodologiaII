"""Persistencia de las solicitudes."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Protocol

from errores import ArchivoDeDatosInvalido
from modelos import Solicitud


class RepositorioSolicitudes(Protocol):
    """Lo que el servicio necesita para leer y guardar solicitudes."""

    def cargar_todas(self) -> list[Solicitud]:
        """Devuelve todas las solicitudes guardadas."""

    def guardar_todas(self, solicitudes: list[Solicitud]) -> None:
        """Guarda la lista completa de solicitudes."""


class RepositorioJSON:
    """Guarda las solicitudes en un archivo JSON."""

    def __init__(self, ruta: str) -> None:
        self._ruta = Path(ruta)

    def cargar_todas(self) -> list[Solicitud]:
        """Lee el archivo; si todavía no existe, devuelve una lista vacía."""
        if not self._ruta.exists():
            return []
        try:
            with self._ruta.open("r", encoding="utf-8") as archivo:
                return [Solicitud.desde_dict(datos) for datos in json.load(archivo)]
        except (ValueError, KeyError, TypeError) as error:
            raise ArchivoDeDatosInvalido(self._ruta.name) from error

    def guardar_todas(self, solicitudes: list[Solicitud]) -> None:
        """Reescribe el archivo con la lista completa de solicitudes."""
        with self._ruta.open("w", encoding="utf-8") as archivo:
            json.dump([s.a_dict() for s in solicitudes], archivo, ensure_ascii=False, indent=2)
