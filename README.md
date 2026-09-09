# PB-RAG-ASISTENTE-TARIFAS-ATM-BCN
Asistente de tarifas y abonos para la red ATM de Barcelona - sistema tarifario integrado que permite utilizar diferentes medios de transporte (metro, autobuses, Ferrocarrils y Rodalies). No es asistente de rutas, solo tarifas y abonos. Solo asiste tarifas de a ATM, no asiste tarifas de medio de transporte individual.

## Estructura del proyecto

```text
PB-RAG-ASISTENTE-TARIFAS-ATM-BCN/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── config.py
├── main.py                   # CLI: prepare / index / query / ask.
├── app.py                    # Streamlit.
├── common/                   # Carpeta donde guardamos ficheros comunes como comfig o utils.
│   ├── config.py             # Se definen parametros generales del sistema.
│   └── utils.py              # Funciones genéricas auxiliares y reutilizables.
├── core/                     # Carpeta donde guardamos los ficheros de la capa de negocio.
│   ├── pipeline.py           # Orquestador de la ingesta y otras llamadas.
│   ├── load.py
│   ├── chunk.py
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
| 1 | `01_Municipios_por_zona.csv` | [mapa-zonas](https://www.tmb.cat/es/tarifas-metro-bus-barcelona/mapa-zonas) |
| 2 | `02_Municipios_tarifa_metropolitana.csv` | [mapa-zonas](https://www.tmb.cat/es/tarifas-metro-bus-barcelona/mapa-zonas) |
| 3 | `11_Intro_sistema_tarifario_integrado.pdf` | [mapa-zonas](https://www.tmb.cat/es/tarifas-metro-bus-barcelona/mapa-zonas) |
| 4 | `12_sistema_tarifario_integrado.pdf` | [sistema tarifario ATM](https://www.atm.cat/es/titols-tarifes/sistema-de-transport/funcionament-del-sistema-tarifari-integrat) |
| 5 | `21_Tarifa_metropolitana.pdf` | [mapa-zonas](https://www.tmb.cat/es/tarifas-metro-bus-barcelona/mapa-zonas) |
| 6 | `22_tarifas_transporte_abonos_normales.csv` | [tarifas TMB](https://www.tmb.cat/es/tarifas-metro-bus-barcelona/precios-titulos-transporte) y [tarifas ATM](https://www.atm.cat/es/titols-tarifes/titols-i-tarifes/titols-principals)|
| 7 | `23_Descripcion_tipos_billetes_ATM.pdf` | [tarifas ATM](https://www.atm.cat/es/titols-tarifes/titols-i-tarifes/titols-principals)|
| 8 | `24_Descripcion_tipos_billetes_TMB.pdf` | [tarifas TMB](https://www.tmb.cat/es/tarifas-metro-bus-barcelona/precios-titulos-transporte)|
| 9 | `25_Otros_titulos_integrados_y_sus_tarifas.pdf` | [tarifas TMB](https://www.tmb.cat/es/tarifas-metro-bus-barcelona/precios-titulos-transporte) y [tarifas ATM](https://www.atm.cat/es/titols-tarifes/titols-i-tarifes/titols-principals)|
| 10 | `31_Condiciones_de_uso_titulos_transporte.pdf` | [Condiciones uso](https://www.tmb.cat/es/tarifas-metro-bus-barcelona/condiciones-uso-billetes) |
| 11 | `32_Preguntas_frecuentes.pdf` | [FAQ](https://www.tmb.cat/es/atencion-al-cliente/preguntas-frecuentes) |

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
  python main.py --prepare                  # Ingesta + embeddings
  python main.py --index                    # Indexar en ChromaDB
  python main.py --index --recreate-index   # Borra la colección de ChromaDB antes de indexar
  python main.py --query "pregunta"         # Pregunta de prueba (retrieval + contexto)
  python main.py --ask "pregunta"           # RAG completo: respuesta generada
  ```

### Paso 4: main.py



## Q&A: Preguntas de ejemplo y resultado esperado

En este apartado se describe una serie de preguntas a realizar al asistente y el resultado esperado.

| Nº | Pregunta | Respuesta esperada |
|---------|-----------|--------------|
| 1 | TBD | TBD|
| 2 | TBD | TBD|
| 3 | TBD | TBD|
| 4 | TBD | TBD|
| 5 | TBD | TBD|




