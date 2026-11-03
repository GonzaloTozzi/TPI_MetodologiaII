"""Punto de entrada: arma las dependencias y arranca la consola."""

import sys

from consola import Consola
from errores import ArchivoDeDatosInvalido
from repositorio import RepositorioJSON
from servicio import ServicioSolicitudes

ARCHIVO_DATOS = "solicitudes.json"


def main() -> int:
    """Devuelve 1 si el archivo de datos está dañado y 0 al salir normalmente."""
    try:
        servicio = ServicioSolicitudes(RepositorioJSON(ARCHIVO_DATOS))
    except ArchivoDeDatosInvalido as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    Consola(servicio).ejecutar()
    return 0


if __name__ == "__main__":
    sys.exit(main())
