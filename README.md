# PB-RAG-ASISTENTE-TARIFAS-ATM-BCN
Asistente de tarifas y abonos para la red ATM de Barcelona - sistema tarifario integrado que permite utilizar diferentes medios de transporte (metro, autobuses, Ferrocarrils y Rodalies). No es asistente de rutas, solo tarifas y abonos. Solo asiste tarifas de a ATM, no asiste tarifas de medio de transporte individual.

Para calcular las zonas por las que pasa un trayecto redirigirá a https://www.atm.cat/es/titols-tarifes/sistema-de-transport/mapa-de-la-zonificacio

## Decisiones técnicas

* La estructura de ficheros y modularización es similar a la propuesta por la academia, pero el empaquetado de los ficheros se ha modificado, haciendo que cada código fuente se ubique dentro de una carpeta según su especialización.
* El 90% de la nomenclatura de los ficheros sigue la propuesta de la academía, aunque se han hecho algunos cambios. Por ejemplo: rag_services.py incluye los servicios de backend que se llamarán desde el frontend.
* Se ha mentenido la estructura *--prepare* donde se genera ingesta y embedding en ficheros, e *--index* donde se genera el indice ChromaDB desde los ficheros para seguir la estructura propuesta por la académia y sobre todo porque esta configuración permite hacer ajustes sobre parámetros de la BBDD ChromaDB sin tener que regenerar el embedding, no obstante en un entorno de producción se considera adecuado unificar los 3 apartados en el *--prepare* para no generar el fichero embeddings.json y que siempre haga borrado de indice (por tanto también dejaría de tener sentido *--recreate-index*)

## Incidencias o peculiaridades del proyecto
* **Separar ingesta y embedding y unir con index:** Se replanteo la posibilidad de que *--prepare* solo generase ingesta e *--index* hiciera embedding e indexación para evitar generar embeddings.json pero por practicidad se descartó.
* **Problema con csv municipios:** Se tuvo que reescribir la ingesta de 01_Municipios_por_zona_y_tarifa_metropolitana.csv ya que generaba un chunk por fila, siendo un chunk muy pequeño dando problemas en el retriever (*--query*) con TOP-K muy pequeños. Se rehizo la construcción del chunk. Se sustituyó cargar_csv_municipios (que se ha dejado comentado a nivel didactico) por cargar_csv_municipios_por_zona.
* 
* Se tuvo que añadir un sleep de 60 segundos entre lotes de embeddings (embeddear_textos de embed.py) porque saturaba la cuota del free tier de google.

## Estructura del proyecto

Si bien la modularización de ficheros es bastante similar a la propuesta por la academia, he seguido una paquetización diferente y más acorde con lo hecho en proyectos pasados realizados por mí.

```text
PB-RAG-ASISTENTE-TARIFAS-ATM-BCN/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── main.py                   # CLI: prepare / index / query / ask.
├── app.py                    # Streamlit.
├── common/                   # Carpeta donde guardamos ficheros comunes como comfig o utils.
│   ├── config.py             # Se definen parametros generales del sistema.
│   └── utils.py              # Funciones genéricas auxiliares y reutilizables.
├── core/                     # Carpeta donde guardamos los ficheros de la capa de negocio.
│   ├── pipeline.py           # Orquestador de la ingesta y otras llamadas.
│   ├── load.py               # Revisa los ficheros del corpues y lo carga con metadatos.
│   ├── chunk.py              # Construye los chunks
│   ├── embed.py
│   ├── index.py
│   ├── retrieve.py
│   └── generate.py
├── data/                     # Corpus
├── entregables/              # informe final del equipo
│   └── informe_decisiones.md
├── llm/                      # Carpeta donde se encuentran los procesos particulares de llamadas a LLM.
│   └── gemini_auth.py        # Carga de API key de gemini
├── output/                   # Ficheros generados entre ellos el indice de chromaDB
├── queries/                  # preguntas de evaluación
└── services/                 # Carpeta donde se encuentras los servicios que llamara Streamlit u otros.
    └── rag_service.py        # Servicios relacionados con RAG. 


```

## Corpus

Descripción de los ficheros y documentos incluidos en el corpues y de donde se han extraido.

Todos los datos son públicos.

| Nº | Fichero | Fuente |
|---------|-----------|--------------|
| 1 | `01_Municipios_por_zona_y_tarifa_metropolitana.csv` | [mapa-zonas](https://www.tmb.cat/es/tarifas-metro-bus-barcelona/mapa-zonas) |
| 2 | `11_Intro_sistema_tarifario_integrado.pdf` | [mapa-zonas](https://www.tmb.cat/es/tarifas-metro-bus-barcelona/mapa-zonas) |
| 3 | `12_sistema_tarifario_integrado.pdf` | [sistema tarifario ATM](https://www.atm.cat/es/titols-tarifes/sistema-de-transport/funcionament-del-sistema-tarifari-integrat) |
| 4 | `21_Tarifa_metropolitana.pdf` | [mapa-zonas](https://www.tmb.cat/es/tarifas-metro-bus-barcelona/mapa-zonas) |
| 5 | `22_tarifas_transporte_abonos_normales.csv` | [tarifas TMB](https://www.tmb.cat/es/tarifas-metro-bus-barcelona/precios-titulos-transporte) y [tarifas ATM](https://www.atm.cat/es/titols-tarifes/titols-i-tarifes/titols-principals)|
| 6 | `23_Descripcion_tipos_billetes_ATM.pdf` | [tarifas ATM](https://www.atm.cat/es/titols-tarifes/titols-i-tarifes/titols-principals)|
| 7 | `24_Descripcion_tipos_billetes_TMB.pdf` | [tarifas TMB](https://www.tmb.cat/es/tarifas-metro-bus-barcelona/precios-titulos-transporte)|
| 8 | `25_Otros_titulos_integrados_y_sus_tarifas.pdf` | [tarifas TMB](https://www.tmb.cat/es/tarifas-metro-bus-barcelona/precios-titulos-transporte) y [tarifas ATM](https://www.atm.cat/es/titols-tarifes/titols-i-tarifes/titols-principals)|
| 9 | `31_Condiciones_de_uso_titulos_transporte.pdf` | [Condiciones uso](https://www.tmb.cat/es/tarifas-metro-bus-barcelona/condiciones-uso-billetes) |
| 10 | `32_Preguntas_frecuentes.pdf` | [FAQ](https://www.tmb.cat/es/atencion-al-cliente/preguntas-frecuentes) |

## Proceso de desarrollo
En este apartado se describe como ha sido el proceso de construcción del proyecto, desde la primera toma de decisón hasta la entrega final.

### Paso 1: ¿Que va a hacer el proyecto y cual será el corpus?

El proyecto consistirá en un asistente de tarifas y abonos para la red ATM (Autoridad de Transporte Metropolitano) de Barcelona que se encarga de gestionar el sistema tarifario integrado que permite utilizar diferentes medios de transporte (metro, autobuses, tranvía, Ferrocarrils y Rodalies) de la Gran Area Metropolitana de Barceelona.

El objetivo del asistente es que sea capaz de recomendar el abono a escoger según los datos, de edad, ubicació de destino, ubicación origen, además de poder responder preguntas sobre condiciones de uso.

No es un asitente de rutas. Solo de tarifas y abonos. Si bien será capaz de responder cual es el abono a adquirir en trayectos entre dos ciudades dentro de la red, no es capaz de devolver ni la mejor ruta, ni información sobre paradas. Igualmente el asistente dará información basada en la zona de cada parada (origen y destino), pero es posible que exista una ruta que requiera pasar por menos zonas pudiendo adquirir un billete más barato.

Dado que la red integrada de ATM está directamente relacionada con TMB (Transporte Metropolitáno de Barcelona) que depende de AMB (Área Metropolitana de Barcelona), se incluirá información de esta última para darle consistencia al asistente, pero el objetivo del mismo es dar información sobre billetes integrados, y no sobre los billetes NO integrados de la redes particulares de FCG (Ferrocarriles Catalanes de la Generalitat), Rodalías (Cercanías de Cataluña), Tramvia y Autobuses (ni metropolitanos, urbanos o interurbanos).

El motivo de no incluir información de paradas o de los billetes no integrados es para no complicar el proyecto y no tener un corpus que supere los 20 documentos estipulados por la academía.

### Paso 2: Descubrimiento y extracción de datos.

Si bien existen páginas [developer.tmb.cat](https://developer.tmb.cat/) o [opendata-ajuntament.barcelona.cat](http://opendata-ajuntament.barcelona.cat/), la información que devuelve es muy específica sobre paradas, líneas o incidencias y no se han utilizado.

Finalmente las fuentes más fiables y desde donde se ha podido recopilar toda la información son:

* https://www.tmb.cat
* https://www.atm.cat
  
### Paso 3: Curado de datos y transformación final para su uso.

Se ha generado un csv con la lista de municipios incluidos dentro del ATM, la zona a la que pertenen y el sector (que hace que aún siendo de la misma implicará comprar billete de varios sectores), otra con la lista de municipios de que están incluidas dentro de la tarifa metropolitan aún siendo de sectores diferentes, y un csv con los abonos y sus tarifas según sector.

Además se incluye pdf con la explicación de como funciona el sistema tarifario y la tarifa metropolitana. Documento con explicación de cada uno de los abonos. Documento con condiciones de uso general y documento con preguntas frecuentes.

### Paso 4: main.py
Se genera el main.py con los parametros de entrada esperados según lo solicitado:

```text
  python main.py --prepare                 #"Ingesta + embeddings (tiempo estimado de ejecución ~ 10 min)"
  python main.py --solo-ingesta            #"Solo realizar la ingesta sin ejecutar embeddings"
  python main.py --index                   #"Indexar en ChromaDB"
  python main.py --recreate-index          #"Borra la colección de ChromaDB antes de indexar"
  python main.py --query                   #"Pregunta de prueba que solo ataca al retrieval (recuperación de contexto)"
  python main.py --ask                     #"Pregunta con respusta generada por el modelo (RAG completo)"
  python main.py --eval                    #"Evaluación del retrieval con preguntas preestablecidas"
  python main.py --top-k                   #"Sobreescribe TOP-K"
  ```

### Paso 5: se reestructuran las carpetas por responsabilidad

Ver estructura del proyecto.

### Paso 6: Se programa la ingesta y el embedding

Se programa la Ingesta y el embeding que se ejecuta mediante: python main.py --prepare

**Empezamos con la ingesta del corpus**: Se llama a ejecutar_ingesta() de pipeline.py, que su vez llama a las funciones de load.py para crear una lista de documentos cargados.
* Para los pdfs usamos PyPDFLoader de Langchain que coge el texto y genera el metadato. Para los CSVs lo construimos nosotros.
  * En este primer pre-procesado los pdfs se parten por página, y los CSV por filas.
* Hacemos la limpieza de datos.
* Construimos los chunks, calculamos estadisticas y lo almacenamos como un json para su futuro uso.
* Se genera el fichero chunks.json para su uso en el embedding

**Continuamos con el embedding del corpus**: Se llama a ejecutar_embeddings() de embed.py.
* Cargamos la API Key de google.
* Cargamos todos los chunks y se los pasamos al modelo de embedding en paquetes para no saturar al LLM.
  * **<span style="color:red;">NOTA IMPORTANTE:</span>** Entre llamada y del embedding se ha hecho un sleep de 60 segundos ya que he tenido muchos problemas. Este tiempo es parametrizable a través del parametro de sistema EMBEDDING_SLEEP.
* Finalmente se genera el fichero embedding.json para su uso a la hora de generar el indice de Chroma
  * **Nota:** En un entorno de producción no se debería generar este fichero, y se tendría que pasar el resultado al indice de chroma, reunificando estas opciones. No obstante se ha mentenido así por seguir el esquema de la academía y sobre todo porque este sistema (y la estructura del código base) facilita la regeneración del indice sin tener que volver a llamar al embedding.

### Paso 7: Se genera el indice en la BBDD ChromaDB

A grandes rasgos recupera el fichero embedding.json con los indices y los carga en la BBDD ChromaDB.

### Paso 8: Programación opción --query que devuelve los chunks guardados en BBDD por similitud de la pregunta

Programación opción --query que devuelve los chunks guardados en BBDD por similitud de la pregunta.

Básicamente se usa el mismo modelo de embedding que se usó para codificar chromaDB y devuelve los vectores con más similitud.


## Q&A: Preguntas de ejemplo y resultado esperado

En este apartado se describe una serie de preguntas a realizar al asistente y el resultado esperado.

| Nº | Pregunta | Respuesta esperada |
|---------|-----------|--------------|
| 1 | TBD | TBD|
| 2 | TBD | TBD|
| 3 | TBD | TBD|
| 4 | TBD | TBD|
| 5 | TBD | TBD|

## Cosas a mejorar del sistema

1.- Separar el embedding del corpus de la ingesta y unificarlo con la indexación de la BBDD ChromaBD (por supuesto modularizadamente) y dejar de generar el fichero embedding.json ya que no solo no aporta nada sino que ocupa espacio. Igualmente hay que dejar la opción de regenerar indice por si hay cambios de parametros pero no de embbeding.

2.- Ajustar el tiempo de sleep entre embbedings del corpus para que se más eficiente.




