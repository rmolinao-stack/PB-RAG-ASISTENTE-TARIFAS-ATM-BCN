""" En este fichero se definen los parametros de configuración globales de todo el proyecto."""

from pathlib import Path

# --- Ingesta y chunking ---
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150 # Aplicamos un 15% del tamaño del chunk.

DATA_DIR = Path(__file__).parent.parent / "data"
OUTPUT_DIR = Path(__file__).parent.parent / "output"
CHUNKS_JSON = OUTPUT_DIR / "chunks.json"
EMBEDDINGS_JSON = OUTPUT_DIR / "embeddings.json"

EMBEDDING_MODEL = "gemini-embedding-2"
MAX_CHUNKS_EMBED: int | None = None  # None = embeddear todos los chunks
EMBED_BATCH_SIZE = 50 # Para enviar lotes de información en paquetes a la API de embeddings y no saturarla.
EMBEDDING_SLEEP = 60 # Segundos de espera entre lotes de embeddings para no saturar la API.

EXTENSIONES_TEXTO = {".txt", ".md"}
EXTENSIONES_PDF = {".pdf"}
EXTENSIONES_CSV = {".csv"}

