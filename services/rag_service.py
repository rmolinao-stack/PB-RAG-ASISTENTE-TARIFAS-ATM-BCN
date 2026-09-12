""" Aquí vamos a incluir los servicios relacionados 
con RAG (Retrieval-Augmented Generation) 
para el asistente de tarifas de ATM BCN.

El frontend (o quien los consuma) llamará a estas funciones.
"""

from core.retriever import recuperar
from core.context import formatear_contexto
from core.prompts import build_rag_prompt
from core.generate import generar_respuesta
from common.utils import _extraer_fuentes

def responder(pregunta: str, top_k: int | None = None) -> dict:
    """Pipeline: retrieve → prompt → generate."""
    if not (pregunta or "").strip():
        return {
            "respuesta": "",
            "contexto": "",
            "chunks": [],
            "fuentes": [],
            "error": "La pregunta no puede estar vacía.",
        }

    chunks = recuperar(pregunta.strip(), top_k=top_k)
    contexto = formatear_contexto(chunks)
    prompt = build_rag_prompt(contexto, pregunta.strip())
    respuesta = generar_respuesta(prompt)

    return {
        "respuesta": respuesta,
        "contexto": contexto,
        "chunks": chunks,
        "fuentes": _extraer_fuentes(chunks),
        "error": None,
    }

def rag_ask(consulta: str) -> str:
    """Pendiente documentar."""
    print("rag_ask: Pendiente de realizar")    
    return None