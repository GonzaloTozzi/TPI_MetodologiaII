class ErrorSolicitudes(Exception):
    pass


class DatosInvalidos(ErrorSolicitudes):
    pass


class SolicitudNoEncontrada(ErrorSolicitudes):
    def __init__(self, identificador: int) -> None:
        super().__init__(f"no existe una solicitud con ID {identificador}.")


class ArchivoDeDatosInvalido(ErrorSolicitudes):
    def __init__(self, nombre_archivo: str) -> None:
        super().__init__(
            f"No se pudo leer el archivo {nombre_archivo}: su contenido no es válido."
        )
