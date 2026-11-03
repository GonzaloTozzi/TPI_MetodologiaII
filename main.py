import sys

from consola import Consola
from errores import ArchivoDeDatosInvalido
from repositorio import RepositorioJSON
from servicio import ServicioSolicitudes

ARCHIVO_DATOS = "solicitudes.json"


def main() -> int:
    try:
        servicio = ServicioSolicitudes(RepositorioJSON(ARCHIVO_DATOS))
    except ArchivoDeDatosInvalido as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    Consola(servicio).ejecutar()
    return 0


if __name__ == "__main__":
    sys.exit(main())
