"""Errores propios del sistema de solicitudes."""


class ErrorSolicitudes(Exception):
    """Error base: la consola lo muestra al usuario como mensaje."""


class DatosInvalidos(ErrorSolicitudes):
    """Algún dato ingresado no cumple las reglas del sistema."""


class SolicitudNoEncontrada(ErrorSolicitudes):
    """No existe una solicitud con el ID indicado."""

    def __init__(self, identificador: int) -> None:
        super().__init__(f"no existe una solicitud con ID {identificador}.")


class ArchivoDeDatosInvalido(ErrorSolicitudes):
    """El archivo de datos existe pero su contenido no se puede leer."""

    def __init__(self, nombre_archivo: str) -> None:
        super().__init__(
            f"No se pudo leer el archivo {nombre_archivo}: su contenido no es válido."
        )
