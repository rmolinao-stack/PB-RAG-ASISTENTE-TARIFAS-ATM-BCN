from langchain_core.documents import Document
from pathlib import Path

from .load import cargar_documentos
from .clean import limpiar_documentos
from common.config import DATA_DIR


def ejecutar_ingesta() -> tuple[list[Document], Path, dict]:
    """Pendiente documentar."""
    print("responder: Pendiente de realizar")    
    return None

def ejecutar_ingesta() -> tuple[list[Document], Path, dict]:
    """Ejecuta la ingesta de documentos y genera los chunks para embeddings."""
    print(f"Ingesta: cargando documentos desde {DATA_DIR} ...")
    crudos = cargar_documentos()
    print(f" Documentos cargados: {len(crudos)}")

    limpios = limpiar_documentos(crudos)
    print(f"  Tras limpieza: {len(limpios)}")

    #for c in limpios:
    #        print(c)
    #        input()

    #chunks = fragmentar_documentos(limpios)
    #print(f"  Chunks generados: {len(chunks)}")

    #stats = calcular_stats_ingesta(crudos, limpios, chunks)
    #ruta = guardar_chunks_json(chunks, CHUNKS_JSON, stats)
    #print(f"  Guardado: {ruta}")

    #imprimir_resumen_consola(chunks, stats)
    #return chunks, ruta, stats