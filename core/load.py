from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from pathlib import Path
import pandas as pd
from common.config import DATA_DIR, EXTENSIONES_PDF, EXTENSIONES_CSV

def valor_celda(fila, columna: str) -> str | None:
    """Lee una celda de un CSV y devuelve su texto, o None si está vacía."""
    if columna not in fila or pd.isna(fila[columna]):
        return None
    texto = str(fila[columna]).strip()
    return texto if texto else None

def fila_a_texto_municipios(fila) -> str | None:
    """Convierte UNA fila del CSV de municipios en texto legible."""

    lineas = [f"Poblacion: {valor_celda(fila, 'Poblacion')}",
              f"Zona Tarifaria: {valor_celda(fila, 'Zona Tarifaria')}",
              f"Sector: {valor_celda(fila, 'Sector') or 'Sin sector'}",
              f"Tarifa Metropolitana: {valor_celda(fila, 'Tarifa Metropolitana')}"]

    return "\n".join(lineas)


def cargar_csv_municipios(ruta: Path) -> list[Document]:
    """Lee el CSV de eventos: un Document por fila con título válido."""
    df = pd.read_csv(ruta, sep=";", encoding="UTF-8", dtype=str)
    documentos: list[Document] = []

    for _, fila in df.iterrows():
        texto = fila_a_texto_municipios(fila)
        if texto is None:
            continue

        metadata: dict = {
            "source": str(ruta),
            "tipo": "zona_tarifaria",  
            "Poblacion": valor_celda(fila, 'Poblacion'),
            "Zona Tarifaria": valor_celda(fila, 'Zona Tarifaria'),
            "Sector": valor_celda(fila, 'Sector') or 'Sin sector',
            "Tarifa Metropolitana": valor_celda(fila, 'Tarifa Metropolitana')
        }
        documentos.append(Document(page_content=texto, metadata=metadata))

    return documentos


def fila_a_texto_tarifas(fila) -> str | None:
    """Convierte UNA fila del CSV de tarifas en texto legible."""

    tarifa_metropolitana = False;
    if valor_celda(fila, 'Tarifa Metropolitana') == "SI":
        tarifa_metropolitana == True;

    lineas = [f"Denominación de tarifa: {valor_celda(fila, 'Titulo')}",
              f"Importe zona 1: {valor_celda(fila, '1 zona')}",
              f"Importe zona 2: {valor_celda(fila, '2 zonas')}",
              f"Importe zona 3: {valor_celda(fila, '3 zonas')}",
              f"Importe zona 4: {valor_celda(fila, '4 zonas')}",
              f"Importe zona 5: {valor_celda(fila, '5 zonas')}",
              f"Importe zona 6: {valor_celda(fila, '6 zonas')}",
              f"Importe zona 7: {valor_celda(fila, '7 zonas')}"
              ]

    return "\n".join(lineas)


def cargar_csv_tarifas(ruta: Path) -> list[Document]:
    """Lee el CSV de eventos: un Document por fila con título válido."""
    df = pd.read_csv(ruta, sep=";", encoding="UTF-8", dtype=str)
    documentos: list[Document] = []

    for _, fila in df.iterrows():
        texto = fila_a_texto_tarifas(fila)
        if texto is None:
            continue

        metadata: dict = {
            "source": str(ruta),
            "tipo": "Tarifas_por_zona",  
            "Denominación de tarifa": valor_celda(fila, 'Titulo'),
            "Importe zona 1": valor_celda(fila, '1 zona'),
            "Importe zona 2": valor_celda(fila, '2 zonas'),
            "Importe zona 3": valor_celda(fila, '3 zonas'),
            "Importe zona 4": valor_celda(fila, '4 zonas'),
            "Importe zona 5": valor_celda(fila, '5 zonas'),
            "Importe zona 6": valor_celda(fila, '6 zonas'),
            "Importe zona 7": valor_celda(fila, '7 zonas')
        }
        documentos.append(Document(page_content=texto, metadata=metadata))

    return documentos

def cargar_archivo(ruta: Path) -> list[Document]:
    """Elige el loader según la extensión del archivo."""
    sufijo = ruta.suffix.lower()

    print(f"La ruta del archivo a cargar es: {ruta}")

    if sufijo in EXTENSIONES_PDF:
        return PyPDFLoader(str(ruta)).load()

    if sufijo in EXTENSIONES_CSV:
        if (ruta.name == "01_Municipios_por_zona_y_tarifa_metropolitana.csv"):
            return cargar_csv_municipios(ruta)
        elif (ruta.name == "22_tarifas_transporte_abonos_normales.csv"):
            return cargar_csv_tarifas(ruta)
        else:
            print(f"Archivo CSV no reconocido: {ruta.name}")
        
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
