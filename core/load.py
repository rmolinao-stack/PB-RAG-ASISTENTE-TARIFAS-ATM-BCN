from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from pathlib import Path
from common.config import DATA_DIR, EXTENSIONES_PDF, EXTENSIONES_CSV



def cargar_archivo(ruta: Path) -> list[Document]:
    """Elige el loader según la extensión del archivo."""
    sufijo = ruta.suffix.lower()

    if sufijo in EXTENSIONES_PDF:
        return PyPDFLoader(str(ruta)).load()

    #if sufijo in EXTENSIONES_CSV:
    # TBD
    # FUNCION QUE CARGA CSV PARTICULARIZADO PARA ESTE PROYECTO
        

    return []

def cargar_documentos() -> list[Document]:
    """Recorre data/ y concatena todos los Document soportados."""
    if not DATA_DIR.exists():
        raise FileNotFoundError(f"No existe la carpeta de datos: {DATA_DIR}")

    documentos: list[Document] = []

    for ruta in sorted(DATA_DIR.rglob("*")):
        if not ruta.is_file():
            continue

        docs = cargar_archivo(ruta)
        if docs:
            print(f"  Cargado: {ruta.name} ({len(docs)} documento(s))")
            documentos.extend(docs)
        elif ruta.suffix:
            print(f"  [omitido] extensión no soportada: {ruta.name}")

    return documentos
