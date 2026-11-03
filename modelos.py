from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from typing import Optional

from errores import DatosInvalidos


class OpcionDeTexto(Enum):
    @classmethod
    def valores(cls) -> list[str]:
        return [opcion.value for opcion in cls]

    @classmethod
    def desde_texto(cls, texto: str):
        buscado = texto.strip().lower()
        for opcion in cls:
            if opcion.value.lower() == buscado:
                return opcion
        raise DatosInvalidos(cls.mensaje_invalido())

    @classmethod
    def mensaje_invalido(cls) -> str:
        valores = cls.valores()
        opciones = ", ".join(valores[:-1]) + " o " + valores[-1]
        return f"{cls.nombre_campo()} debe ser {opciones}."

    @classmethod
    def nombre_campo(cls) -> str:
        raise NotImplementedError


class Estado(OpcionDeTexto):
    PENDIENTE = "Pendiente"
    EN_PROCESO = "En proceso"
    RESUELTA = "Resuelta"

    @classmethod
    def nombre_campo(cls) -> str:
        return "el estado"


class Prioridad(OpcionDeTexto):
    BAJA = "Baja"
    MEDIA = "Media"
    ALTA = "Alta"

    @classmethod
    def nombre_campo(cls) -> str:
        return "la prioridad"


def correo_valido(correo: str) -> bool:
    correo = correo.strip()
    usuario, _, dominio = correo.partition("@")
    return bool(usuario) and "." in dominio and " " not in correo


def exigir_texto(valor: str, mensaje: str) -> None:
    if not valor.strip():
        raise DatosInvalidos(mensaje)


@dataclass
class Estudiante:
    nombre: str
    correo: str


@dataclass
class Responsable:
    nombre: str
    area: str

    def validar(self) -> None:
        exigir_texto(self.nombre, "el nombre del responsable es obligatorio.")

    def __str__(self) -> str:
        return f"{self.nombre} ({self.area})" if self.area.strip() else self.nombre


@dataclass
class DatosSolicitud:
    estudiante: Estudiante
    tipo: str
    descripcion: str
    prioridad: str

    def validar(self) -> None:
        exigir_texto(self.estudiante.nombre, "el nombre del estudiante es obligatorio.")
        if not correo_valido(self.estudiante.correo):
            raise DatosInvalidos("el correo no es válido.")
        exigir_texto(self.tipo, "el tipo de solicitud es obligatorio.")
        exigir_texto(self.descripcion, "la descripción es obligatoria.")


@dataclass
class Solicitud:
    id: int
    estudiante: Estudiante
    tipo: str
    descripcion: str
    prioridad: str
    estado: Estado = Estado.PENDIENTE
    responsable: Optional[Responsable] = None

    @classmethod
    def nueva(cls, identificador: int, datos: DatosSolicitud) -> Solicitud:
        datos.validar()
        return cls(
            id=identificador,
            estudiante=datos.estudiante,
            tipo=datos.tipo,
            descripcion=datos.descripcion,
            prioridad=Prioridad.desde_texto(datos.prioridad).value,
        )

    def cambiar_estado(self, estado: Estado) -> None:
        self.estado = estado

    def asignar_responsable(self, responsable: Responsable) -> None:
        responsable.validar()
        self.responsable = responsable

    def linea_listado(self) -> str:
        responsable = str(self.responsable) if self.responsable else "Sin asignar"
        return (
            f"#{self.id} | {self.estudiante.nombre} | {self.tipo} | {self.prioridad} | "
            f"{self.estado.value} | Responsable: {responsable}"
        )

    def linea_resumen(self) -> str:
        return f"#{self.id}: {self.descripcion} ({self.estado.value})"

    def a_dict(self) -> dict:
        return {
            "id": self.id,
            "estudiante": asdict(self.estudiante),
            "tipo": self.tipo,
            "descripcion": self.descripcion,
            "prioridad": self.prioridad,
            "estado": self.estado.value,
            "responsable": asdict(self.responsable) if self.responsable else None,
        }

    @classmethod
    def desde_dict(cls, datos: dict) -> Solicitud:
        responsable = datos["responsable"]
        return cls(
            id=datos["id"],
            estudiante=Estudiante(**datos["estudiante"]),
            tipo=datos["tipo"],
            descripcion=datos["descripcion"],
            prioridad=datos["prioridad"],
            estado=Estado(datos["estado"]),
            responsable=Responsable(**responsable) if responsable else None,
        )
