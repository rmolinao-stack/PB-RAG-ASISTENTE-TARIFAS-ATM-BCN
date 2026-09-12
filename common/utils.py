from pathlib import Path

def _extraer_fuentes(chunks: list[dict]) -> list[str]:
    fuentes: list[str] = []
    vistos: set[str] = set()
    for chunk in chunks:
        source = chunk.get("metadata", {}).get("source", "?")
        nombre = Path(str(source)).name
        if nombre not in vistos:
            vistos.add(nombre)
            fuentes.append(nombre)
    return fuentes