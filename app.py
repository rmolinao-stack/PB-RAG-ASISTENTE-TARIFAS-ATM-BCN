"""Interfaz Streamlit 
  streamlit run app.py
"""

from __future__ import annotations

import time
from collections.abc import Iterator

import streamlit as st

from common.config import TOP_K
from services.rag_service import responder


def stream_palabras(texto: str, delay: float = 0.02) -> Iterator[str]:
    """Genera el texto palabra a palabra (efecto 'máquina de escribir').
    """
    for palabra in texto.split():
        yield palabra + " "
        time.sleep(delay)


def mensaje_bienvenida(nombre: str) -> dict:
    """Primer mensaje del asistente al abrir (o al limpiar) el chat.

    Devuelve un dict con la misma forma que el resto del historial
    (role, content, fuentes, contexto, error) para poder pintarlo
    con `render_mensaje` sin casos especiales.
    """
    return {
        "role": "assistant",
        "content": (
            f"Hola — soy **{nombre}**. "
            "Pregúntame sobre las tarifas y abonos de la red ATM de Barcelona. "
            "No mantengo el contexto entre preguntas."
        ),
        "fuentes": [],
        "contexto": "",
        "modelo": "",
        "tiempo_ms": 0,
        "error": False,
    }


def render_mensaje(message: dict) -> None:
    """Pinta un mensaje del historial en la UI (usuario o asistente).

    - Texto principal (o `st.error` si hubo fallo).
    - Fuentes bajo la respuesta (trazabilidad del retrieval).
    - Expander con el contexto recuperado.
    """
    with st.chat_message(message["role"]):
        if message.get("error"):
            st.error(message["content"])
        else:
            st.markdown(message["content"])

            # Pinta modelo y tiempo si existen en el mensaje del historial
            modelo = message.get("modelo")
            tiempo_ms = message.get("tiempo_ms")
            if modelo or tiempo_ms:
                st.caption(f"🤖 {modelo or 'N/A'} · ⏱️ {tiempo_ms or 0} ms")

        if message.get("fuentes"):
            st.markdown("**Fuentes**")
            for fuente in message["fuentes"]:
                st.write(f"- `{fuente}`")

        if message.get("contexto"):
            with st.expander("Contexto recuperado (debug)"):
                st.text(message["contexto"])


# --- Configuración de la página (título de la pestaña del navegador) ---
st.set_page_config(
    page_title="Asistente de tarifas y abonos ATM",
    page_icon="🚆",
    layout="centered",
)

# --- Sidebar: controles que no van en el hilo del chat ---
with st.sidebar:
    st.header("Configuración")
    nombre_bot = st.text_input("Nombre del bot", value="Asistente de tarifas y abonos ATM")
    # top_k se pasa a responder(); cambia cuántos chunks recupera el retriever
    top_k = st.slider("Top-K (chunks)", min_value=1, max_value=5, value=TOP_K)
    st.caption("Índice: `output/chroma_db/` (ejecuta `python main.py --prepare --index`).")
    if st.button("Limpiar chat", use_container_width=True):
        # Reinicia el historial; el modelo no “olvida” nada porque cada turno es independiente
        st.session_state.messages = [mensaje_bienvenida(nombre_bot)]
        st.rerun()

st.title(nombre_bot)
st.caption(
    "Asistente de tarifas y abonos ATM"
)

# --- Historial en session_state (sobrevive a cada rerun de Streamlit) ---
if "messages" not in st.session_state:
    st.session_state.messages = [mensaje_bienvenida(nombre_bot)]

# Repintar todo el hilo en cada ejecución del script
for message in st.session_state.messages:
    render_mensaje(message)

# --- Nuevo mensaje del usuario ---
if prompt := st.chat_input("Tu pregunta sobre las tarifas y abonos de la red ATM de Barcelona…"):
    # 1) Guardar y mostrar la pregunta
    st.session_state.messages.append(
        {"role": "user", "content": prompt, "fuentes": [], "contexto": "", "error": False}
    )
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2) Llamar al backend RAG (una pregunta → un dict; sin memoria de conversación)
    with st.chat_message("assistant"):
        with st.status("Consultando el corpus…", expanded=False) as status:
            resultado = responder(prompt, top_k=top_k)
            status.update(label="Listo", state="complete")

        if resultado.get("error"):
            # Validación, índice vacío, API, etc. → mensaje amigable
            st.error(resultado["error"])
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": resultado["error"],
                    "fuentes": resultado.get("fuentes") or [],
                    "contexto": resultado.get("contexto") or "",
                    "modelo": resultado.get("modelo") or "",
                    "tiempo_ms": resultado.get("tiempo_ms") or 0,
                    "error": True,
                }
            )
        else:
            # 3) Mostrar respuesta con streaming; luego fuentes y contexto
            escrito = st.write_stream(stream_palabras(resultado["respuesta"]))
            contenido = escrito if isinstance(escrito, str) else resultado["respuesta"]

            #print(f"Modelo: {resultado.get('modelo') or 'kk'} · Tiempo (ms): {resultado.get('tiempo_ms') or 'kk'}")

            modelo = resultado.get("modelo") or ""
            tiempo_ms = resultado.get("tiempo_ms") or 0
            if modelo or tiempo_ms:
                st.caption(f"🤖 {modelo} · ⏱️ {tiempo_ms} ms")

            if resultado.get("fuentes"):
                st.markdown("**Fuentes**")
                for fuente in resultado["fuentes"]:
                    st.write(f"- `{fuente}`")

            if resultado.get("contexto"):
                with st.expander("Contexto recuperado (debug)"):
                    st.text(f"Modelo: {resultado.get('modelo') or ''}")
                    st.text(f"Tiempo de respuesta (ms): {resultado.get('tiempo_ms') or 0}")
                    st.text(resultado["contexto"])

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": contenido,
                    "fuentes": resultado.get("fuentes") or [],
                    "contexto": resultado.get("contexto") or "",
                    "modelo": modelo,
                    "tiempo_ms": tiempo_ms,
                    "error": False,
                }
            )
