import json
import os
from enum import Enum

ARCHIVO = "solicitudes.json"


class Estado(Enum):
    PENDIENTE = "Pendiente"
    EN_PROCESO = "En proceso"
    RESUELTA = "Resuelta"

    @classmethod
    def valores(cls):
        return [estado.value for estado in cls]


def cargar():
    if not os.path.exists(ARCHIVO):
        return []
    with open(ARCHIVO, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def guardar(solicitudes):
    with open(ARCHIVO, "w", encoding="utf-8") as archivo:
        json.dump(solicitudes, archivo, ensure_ascii=False, indent=2)


def registrar(solicitudes, estudiante, correo, tipo, descripcion, prioridad):
    if not estudiante.strip() or not descripcion.strip():
        return False
    nuevo_id = max((s["id"] for s in solicitudes), default=0) + 1
    solicitudes.append({"id": nuevo_id, "estudiante": {"nombre": estudiante, "correo": correo},
                       "tipo": tipo, "descripcion": descripcion, "prioridad": prioridad,
                       "estado": Estado.PENDIENTE.value, "responsable": None})
    guardar(solicitudes)
    return True


def listar(solicitudes):
    if not solicitudes:
        print("No hay solicitudes.")
    for s in solicitudes:
        print(f'#{s["id"]} | {s["estudiante"]["nombre"]} | {s["tipo"]} | {s["prioridad"]} | {s["estado"]} | Responsable: {s["responsable"] or "Sin asignar"}')


def buscar_por_id(solicitudes, identificador):
    for s in solicitudes:
        if s["id"] == identificador:
            return s
    return None


def cambiar_estado(solicitudes, identificador, estado):
    if estado not in Estado.valores():
        return False
    solicitud = buscar_por_id(solicitudes, identificador)
    if solicitud is None:
        return False
    solicitud["estado"] = estado
    guardar(solicitudes)
    return True


def asignar(solicitudes, identificador, nombre, area):
    solicitud = buscar_por_id(solicitudes, identificador)
    if solicitud is None or not nombre.strip():
        return False
    solicitud["responsable"] = {"nombre": nombre, "area": area}
    guardar(solicitudes)
    return True


def filtrar(solicitudes, estado):
    for s in solicitudes:
        if s["estado"].lower() == estado.lower():
            print(f'#{s["id"]}: {s["descripcion"]} ({s["estado"]})')


def reporte(solicitudes):
    print(f"Total: {len(solicitudes)}")
    for estado in Estado:
        cantidad = sum(1 for s in solicitudes if s["estado"] == estado.value)
        print(f"{estado.value}: {cantidad}")


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
    estudiante = input("Estudiante: ")
    correo = input("Correo: ")
    tipo = input("Tipo de solicitud: ")
    descripcion = input("Descripción: ")
    prioridad = input("Prioridad (Baja/Media/Alta): ")
    if registrar(solicitudes, estudiante, correo, tipo, descripcion, prioridad):
        print("Registrada.")
    else:
        print("Datos inválidos.")


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
    nombre = input("Responsable: ")
    area = input("Área: ")
    if asignar(solicitudes, identificador, nombre, area):
        print("Asignado.")
    else:
        print("No se pudo asignar.")


def opcion_filtrar(solicitudes):
    filtrar(solicitudes, input("Estado a filtrar: "))


def main():
    solicitudes = cargar()
    while True:
        mostrar_menu()
        opcion = input("Opción: ").strip()
        if opcion == "1":
            opcion_registrar(solicitudes)
        elif opcion == "2":
            listar(solicitudes)
        elif opcion == "3":
            opcion_cambiar_estado(solicitudes)
        elif opcion == "4":
            opcion_asignar(solicitudes)
        elif opcion == "5":
            opcion_filtrar(solicitudes)
        elif opcion == "6":
            reporte(solicitudes)
        elif opcion == "0":
            break
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    main()
