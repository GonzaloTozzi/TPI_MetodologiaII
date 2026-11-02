import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

RAIZ_PROYECTO = Path(__file__).resolve().parent.parent
PROGRAMA = "main.py"
NO_COPIAR = shutil.ignore_patterns(
    ".git",
    ".idea",
    ".vscode",
    ".venv",
    "venv",
    "tests",
    "__pycache__",
    "*.pyc",
    ".pytest_cache",
    "solicitudes.json",
)


class Aplicacion:
    """Copia aislada del proyecto que se usa igual que lo haría una persona."""

    def __init__(self, carpeta):
        self.carpeta = carpeta
        self.archivo_datos = carpeta / "solicitudes.json"

    def ejecutar(self, *entradas):
        """Ejecuta python main.py tipeando las entradas indicadas.

        Al final siempre se elige la opción 0 (Salir) para cerrar el programa.
        """
        texto = "\n".join([*entradas, "0"]) + "\n"
        entorno = dict(os.environ, PYTHONIOENCODING="utf-8")
        return subprocess.run(
            [sys.executable, PROGRAMA],
            input=texto,
            capture_output=True,
            text=True,
            encoding="utf-8",
            cwd=self.carpeta,
            env=entorno,
            timeout=10,
        )


@pytest.fixture
def app(tmp_path):
    """Cada test trabaja sobre su propia copia y nunca toca el solicitudes.json real."""
    carpeta = tmp_path / "app"
    shutil.copytree(RAIZ_PROYECTO, carpeta, ignore=NO_COPIAR)
    return Aplicacion(carpeta)
