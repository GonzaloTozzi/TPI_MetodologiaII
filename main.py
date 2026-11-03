from consola import Consola
from repositorio import RepositorioJSON
from servicio import ServicioSolicitudes

ARCHIVO_DATOS = "solicitudes.json"


def main():
    servicio = ServicioSolicitudes(RepositorioJSON(ARCHIVO_DATOS))
    Consola(servicio).ejecutar()


if __name__ == "__main__":
    main()
