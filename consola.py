from __future__ import annotations

from typing import Optional

from modelos import DatosSolicitud, Estado, Estudiante, Responsable
from servicio import ServicioSolicitudes


class Consola:
    def __init__(self, servicio: ServicioSolicitudes) -> None:
        self._servicio = servicio
        self._opciones = {
            "1": ("Registrar solicitud", self._registrar),
            "2": ("Listar solicitudes", self._listar),
            "3": ("Cambiar estado", self._cambiar_estado),
            "4": ("Asignar responsable", self._asignar_responsable),
            "5": ("Filtrar por estado", self._filtrar),
            "6": ("Reporte", self._reporte),
        }

    def ejecutar(self) -> None:
        while True:
            self._mostrar_menu()
            opcion = input("Opción: ").strip()
            if opcion == "0":
                break
            if opcion in self._opciones:
                _, accion = self._opciones[opcion]
                accion()
            else:
                print("Opción inválida.")

    def _mostrar_menu(self) -> None:
        print("\n=== SOLICITUDES ACADÉMICAS ===")
        for clave, (texto, _) in self._opciones.items():
            print(f"{clave}. {texto}")
        print("0. Salir")

    def _registrar(self) -> None:
        estudiante = Estudiante(nombre=input("Estudiante: "), correo=input("Correo: "))
        datos = DatosSolicitud(
            estudiante=estudiante,
            tipo=input("Tipo de solicitud: "),
            descripcion=input("Descripción: "),
            prioridad=input("Prioridad (Baja/Media/Alta): "),
        )
        print("Registrada." if self._servicio.registrar(datos) else "Datos inválidos.")

    def _listar(self) -> None:
        solicitudes = self._servicio.listar()
        if not solicitudes:
            print("No hay solicitudes.")
        for solicitud in solicitudes:
            print(solicitud.linea_listado())

    def _cambiar_estado(self) -> None:
        identificador = self._leer_id()
        if identificador is None:
            return
        estado = input(f"Estado ({'/'.join(Estado.valores())}): ")
        actualizado = self._servicio.cambiar_estado(identificador, estado)
        print("Actualizado." if actualizado else "No se pudo actualizar.")

    def _asignar_responsable(self) -> None:
        identificador = self._leer_id()
        if identificador is None:
            return
        responsable = Responsable(nombre=input("Responsable: "), area=input("Área: "))
        asignado = self._servicio.asignar_responsable(identificador, responsable)
        print("Asignado." if asignado else "No se pudo asignar.")

    def _filtrar(self) -> None:
        for solicitud in self._servicio.filtrar_por_estado(input("Estado a filtrar: ")):
            print(solicitud.linea_resumen())

    def _reporte(self) -> None:
        print(f"Total: {len(self._servicio.listar())}")
        for estado, cantidad in self._servicio.contar_por_estado().items():
            print(f"{estado.value}: {cantidad}")

    @staticmethod
    def _leer_id() -> Optional[int]:
        try:
            return int(input("ID: "))
        except ValueError:
            print("ID inválido.")
            return None
