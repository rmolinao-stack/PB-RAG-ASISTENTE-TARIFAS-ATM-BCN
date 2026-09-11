"""Punto de entrada del pipeline RAG completo (S8 + S9 + S10).

Uso:
  python main.py --prepare                  # Ingesta + embeddings
  python main.py --index                    # Indexar en ChromaDB
  python main.py --index --recreate-index   # Borra la colección de ChromaDB antes de indexar
  python main.py --query "pregunta"         # Pregunta de prueba (retrieval + contexto)
  python main.py --ask "pregunta"           # RAG completo: respuesta generada
  python main.py --eval                     # Evaluación del retrieval con preguntas preestablecidas


App Streamlit: streamlit run app.py
"""

import argparse
from core.pipeline import ejecutar_ingesta
from core.embed import ejecutar_embeddings

def preparar_ingesta_y_embeddings() -> None:
    ejecutar_ingesta()
    ejecutar_embeddings()

def main() -> None:
    parser = argparse.ArgumentParser(
        description="""
        Asistente de tarifas y abonos para la red ATM de Barcelona -
        sistema tarifario integrado que permite utilizar diferentes medios de transporte 
        (metro, autobuses, Ferrocarrils y Rodalies)
        """
    )
    parser.add_argument("--prepare", action="store_true", help="Ingesta + embeddings (tiempo estimado de ejecución ~ 10 min)")
    parser.add_argument("--index", action="store_true", help="Indexar en ChromaDB")
    parser.add_argument("--recreate-index", action="store_true", help="Borra la colección de ChromaDB antes de indexar")
    parser.add_argument("--query", type=str, help="Pregunta de prueba (retrieval + contexto)")
    parser.add_argument("--ask", type=str, help="RAG completo: respuesta generada")
    parser.add_argument("--eval", action="store_true", help="Evaluación del retrieval con preguntas preestablecidas")
    parser.add_argument("--top-k", type=int, default=None, help="Sobreescribe TOP-K")
    

    args = parser.parse_args()

    if not any(
        [args.prepare, args.index, args.recreate_index, args.query, args.ask, args.eval]
    ):
        parser.print_help()
        print(
            "\nEjemplo:\n"
            "  python main.py --prepare --index\n"
            '  python main.py --ask "¿Cuantos viajes puedo hacer con T-Usual?"\n'
            "  streamlit run app.py"
        )
        return

    if args.prepare:
        print("prepare")
        preparar_ingesta_y_embeddings()
        
        #_cmd_prepare()
    if args.index:
        print("index")
        #_cmd_index(recreate=args.recreate_index)
    if args.query:
        print("query")
        #_cmd_query(args.query, args.top_k)
    if args.ask:
        print("ask")
        #_cmd_ask(args.ask, args.top_k)
    if args.eval:
        print("eval")
        #_cmd_eval()
    

if __name__ == "__main__":
    main()