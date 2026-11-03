from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from typing import Optional


class Estado(Enum):
    PENDIENTE = "Pendiente"
    EN_PROCESO = "En proceso"
    RESUELTA = "Resuelta"

    @classmethod
    def valores(cls) -> list[str]:
        return [estado.value for estado in cls]


@dataclass
class Estudiante:
    nombre: str
    correo: str


@dataclass
class Responsable:
    nombre: str
    area: str


@dataclass
class DatosSolicitud:
    estudiante: Estudiante
    tipo: str
    descripcion: str
    prioridad: str


@dataclass
class Solicitud:
    id: int
    estudiante: Estudiante
    tipo: str
    descripcion: str
    prioridad: str
    estado: Estado = Estado.PENDIENTE
    responsable: Optional[Responsable] = None

    def cambiar_estado(self, estado: Estado) -> None:
        self.estado = estado

    def asignar_responsable(self, responsable: Responsable) -> None:
        self.responsable = responsable

    def linea_listado(self) -> str:
        responsable = asdict(self.responsable) if self.responsable else "Sin asignar"
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
