# PB-RAG-ASISTENTE-TARIFAS-ATM-BCN
Asistente de tarifas y abonos para la red ATM de Barcelona - sistema tarifario integrado que permite utilizar diferentes medios de transporte (metro, autobuses, Ferrocarrils y Rodalies). No es asistente de rutas, solo tarifas y abonos. Solo asiste tarifas de a ATM, no asiste tarifas de medio de transporte individual.

```text
PB-RAG-ASISTENTE-TARIFAS-ATM-BCN/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── config.py
├── main.py                 # CLI: prepare / index / query / ask
├── app.py                  # Streamlit
├── src/
│   ├── load.py
│   ├── chunk.py
│   ├── embed.py
│   ├── index.py
│   ├── retrieve.py
│   ├── generate.py
│   └── logging_utils.py    # o equivalente
├── data/                   # corpus (o instrucciones para descargarlo)
├── queries/                # preguntas de evaluación
├── entregables/            # informe final del equipo
│   └── informe_decisiones.md
└── chroma/ o output/       # índice (gitignored)
```

# Proceso de desarrollo

* Paso 1: Decisión de asistente.
* Paso 2: Descubrimiento de donde extraer datos.
* Paso 3: Extracción de datos.
* Paso 4: Curado de datos y transformación final para su uso.

# Datos

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


