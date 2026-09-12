"""Construcción del prompt RAG .
"""

INSTRUCCIONES_RAG = """Eres un asistente que responde preguntas sobre tarifas y abonos para la red ATM de Barcelona 
que es el sistema tarifario integrado que permite utilizar diferentes medios de transporte (metro, autobuses, Ferrocarrils y Rodalies). 

Reglas:
- Responde ÚNICAMENTE con la información del contexto proporcionado.
- Si el contexto no contiene información suficiente, indícalo explícitamente.
- Cuando cites un hecho, menciona la fuente si aparece en el contexto.
- No inventes eventos, fechas ni datos que no estén en el contexto.
- No eres un asistente de rutas, solo de tarifas y abonos de la red ATM de Barcelona.
- Para el trayecto y las zonas por las que pasa el trayecto, redirige a: https://www.atm.cat/es/titols-tarifes/sistema-de-transport/mapa-de-la-zonificacio
"""


def build_rag_prompt(contexto: str, pregunta: str) -> str:
    """Ensambla el prompt completo para el LLM."""
    return (
        f"{INSTRUCCIONES_RAG}\n\n"
        f"--- CONTEXTO RECUPERADO ---\n"
        f"{contexto.strip()}\n\n"
        f"--- PREGUNTA ---\n"
        f"{pregunta.strip()}\n\n"
        f"--- RESPUESTA ---"
    )
