import json
import os
from dataclasses import asdict, dataclass
from enum import Enum
from typing import Optional

ARCHIVO = "solicitudes.json"


class Estado(Enum):
    PENDIENTE = "Pendiente"
    EN_PROCESO = "En proceso"
    RESUELTA = "Resuelta"

    @classmethod
    def valores(cls):
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

    def cambiar_estado(self, estado):
        self.estado = estado

    def asignar_responsable(self, responsable):
        self.responsable = responsable

    def linea_listado(self):
        responsable = asdict(self.responsable) if self.responsable else "Sin asignar"
        return (
            f"#{self.id} | {self.estudiante.nombre} | {self.tipo} | {self.prioridad} | "
            f"{self.estado.value} | Responsable: {responsable}"
        )

    def linea_resumen(self):
        return f"#{self.id}: {self.descripcion} ({self.estado.value})"

    def a_dict(self):
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
    def desde_dict(cls, datos):
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


def cargar():
    if not os.path.exists(ARCHIVO):
        return []
    with open(ARCHIVO, "r", encoding="utf-8") as archivo:
        return [Solicitud.desde_dict(datos) for datos in json.load(archivo)]


def guardar(solicitudes):
    with open(ARCHIVO, "w", encoding="utf-8") as archivo:
        json.dump([s.a_dict() for s in solicitudes], archivo, ensure_ascii=False, indent=2)


def registrar(solicitudes, datos):
    if not datos.estudiante.nombre.strip() or not datos.descripcion.strip():
        return False
    nuevo_id = max((s.id for s in solicitudes), default=0) + 1
    solicitudes.append(Solicitud(
        id=nuevo_id,
        estudiante=datos.estudiante,
        tipo=datos.tipo,
        descripcion=datos.descripcion,
        prioridad=datos.prioridad,
    ))
    guardar(solicitudes)
    return True


def buscar_por_id(solicitudes, identificador):
    for solicitud in solicitudes:
        if solicitud.id == identificador:
            return solicitud
    return None


def cambiar_estado(solicitudes, identificador, texto_estado):
    if texto_estado not in Estado.valores():
        return False
    solicitud = buscar_por_id(solicitudes, identificador)
    if solicitud is None:
        return False
    solicitud.cambiar_estado(Estado(texto_estado))
    guardar(solicitudes)
    return True


def asignar(solicitudes, identificador, responsable):
    solicitud = buscar_por_id(solicitudes, identificador)
    if solicitud is None or not responsable.nombre.strip():
        return False
    solicitud.asignar_responsable(responsable)
    guardar(solicitudes)
    return True


def filtrar_por_estado(solicitudes, texto_estado):
    return [s for s in solicitudes if s.estado.value.lower() == texto_estado.lower()]


def contar_por_estado(solicitudes):
    return {estado: sum(1 for s in solicitudes if s.estado is estado) for estado in Estado}


def leer_id():
    try:
        return int(input("ID: "))
    except ValueError:
        print("ID inválido.")
        return None


def mostrar_menu():
    print("\n=== SOLICITUDES ACADÉMICAS ===")
    print("1. Registrar solicitud\n2. Listar solicitudes\n3. Cambiar estado")
    print("4. Asignar responsable\n5. Filtrar por estado\n6. Reporte\n0. Salir")


def opcion_registrar(solicitudes):
    estudiante = Estudiante(nombre=input("Estudiante: "), correo=input("Correo: "))
    datos = DatosSolicitud(
        estudiante=estudiante,
        tipo=input("Tipo de solicitud: "),
        descripcion=input("Descripción: "),
        prioridad=input("Prioridad (Baja/Media/Alta): "),
    )
    if registrar(solicitudes, datos):
        print("Registrada.")
    else:
        print("Datos inválidos.")


def opcion_listar(solicitudes):
    if not solicitudes:
        print("No hay solicitudes.")
    for solicitud in solicitudes:
        print(solicitud.linea_listado())


def opcion_cambiar_estado(solicitudes):
    identificador = leer_id()
    if identificador is None:
        return
    estado = input(f"Estado ({'/'.join(Estado.valores())}): ")
    if cambiar_estado(solicitudes, identificador, estado):
        print("Actualizado.")
    else:
        print("No se pudo actualizar.")


def opcion_asignar(solicitudes):
    identificador = leer_id()
    if identificador is None:
        return
    responsable = Responsable(nombre=input("Responsable: "), area=input("Área: "))
    if asignar(solicitudes, identificador, responsable):
        print("Asignado.")
    else:
        print("No se pudo asignar.")


def opcion_filtrar(solicitudes):
    for solicitud in filtrar_por_estado(solicitudes, input("Estado a filtrar: ")):
        print(solicitud.linea_resumen())


def opcion_reporte(solicitudes):
    print(f"Total: {len(solicitudes)}")
    for estado, cantidad in contar_por_estado(solicitudes).items():
        print(f"{estado.value}: {cantidad}")


def main():
    solicitudes = cargar()
    while True:
        mostrar_menu()
        opcion = input("Opción: ").strip()
        if opcion == "1":
            opcion_registrar(solicitudes)
        elif opcion == "2":
            opcion_listar(solicitudes)
        elif opcion == "3":
            opcion_cambiar_estado(solicitudes)
        elif opcion == "4":
            opcion_asignar(solicitudes)
        elif opcion == "5":
            opcion_filtrar(solicitudes)
        elif opcion == "6":
            opcion_reporte(solicitudes)
        elif opcion == "0":
            break
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    main()
