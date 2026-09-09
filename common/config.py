""" En este fichero se definen los parametros de configuración globales de todo el proyecto."""

from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"

EXTENSIONES_TEXTO = {".txt", ".md"}
EXTENSIONES_PDF = {".pdf"}
EXTENSIONES_CSV = {".csv"}