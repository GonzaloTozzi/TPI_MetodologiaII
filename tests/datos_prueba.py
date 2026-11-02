"""Datos ficticios y entradas de teclado que reutilizan los tests."""


def registro(estudiante, correo, tipo, descripcion, prioridad):
    """Entradas de la opción 1 (Registrar solicitud)."""
    return ["1", estudiante, correo, tipo, descripcion, prioridad]


def cambio_estado(identificador, estado):
    """Entradas de la opción 3 (Cambiar estado)."""
    return ["3", identificador, estado]


def asignacion(identificador, nombre, area):
    """Entradas de la opción 4 (Asignar responsable)."""
    return ["4", identificador, nombre, area]


def filtro(estado):
    """Entradas de la opción 5 (Filtrar por estado)."""
    return ["5", estado]


LISTAR = ["2"]
REPORTE = ["6"]

ANA = registro(
    "Ana Pérez",
    "ana.perez@ejemplo.com",
    "Certificado",
    "Certificado de alumno regular",
    "Alta",
)
BRUNO = registro(
    "Bruno Díaz",
    "bruno.diaz@ejemplo.com",
    "Equivalencia",
    "Equivalencia de Programación I",
    "Media",
)
CARLA = registro(
    "Carla Ruiz",
    "carla.ruiz@ejemplo.com",
    "Reclamo",
    "Reclamo por nota de parcial",
    "Baja",
)
