""" En este fichero se definen los parametros de configuración globales de todo el proyecto."""

from pathlib import Path

# --- Ingesta y chunking ---
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150 #Aplicamos un 15% del tamaño del chunk.

DATA_DIR = Path(__file__).parent.parent / "data"
OUTPUT_DIR = Path(__file__).parent.parent / "output"
CHUNKS_JSON = OUTPUT_DIR / "chunks.json"
EMBEDDINGS_JSON = OUTPUT_DIR / "embeddings.json"

EXTENSIONES_TEXTO = {".txt", ".md"}
EXTENSIONES_PDF = {".pdf"}
EXTENSIONES_CSV = {".csv"}

