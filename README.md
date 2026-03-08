# cr-pib-zonas-francas

Análisis de datos sobre la brecha entre el crecimiento del PIB costarricense y la economía cotidiana, con foco en el rol de las zonas francas.

---

## Pregunta central

¿El crecimiento del PIB refleja la realidad económica de la mayoría de los hogares, o está concentrado en un sector desconectado del resto de la economía?

---

## Estructura del repositorio

```
data/raw/          Datos originales sin procesar (BCCR, PROCOMER, INEC, etc.)
data/processed/    Datos limpios y transformados, listos para análisis
notebooks/         Análisis en Jupyter: exploración, brechas y visualizaciones
src/               Funciones utilitarias reutilizables (carga, guardado, rutas)
outputs/           Gráficos generados y reporte final del análisis
```

---

## Fuentes de datos

- **BCCR** – Banco Central de Costa Rica (cuentas nacionales, PIB)
- **PROCOMER** – Promotora del Comercio Exterior (estadísticas de zonas francas)
- **INEC** – Instituto Nacional de Estadística y Censos (hogares, empleo, ingresos)
- **OCDE** – Indicadores de desigualdad y productividad
- **Estado de la Nación** – Informes anuales sobre desarrollo humano sostenible

---

## Los tres actos del análisis

1. **Exploración** (`01_exploracion.ipynb`) — Carga, inspección y limpieza inicial de los datos de PIB, zonas francas y condiciones de los hogares.
2. **Brechas** (`02_brechas.ipynb`) — Cuantificación de la distancia entre el crecimiento agregado del PIB y los indicadores de bienestar de la mayoría de la población.
3. **Visualizaciones** (`03_visualizaciones.ipynb`) — Generación de gráficos para comunicar los hallazgos de forma clara y accesible.

---

## Tecnologías

Python · pandas · matplotlib · seaborn · Jupyter

---

*Proyecto de [MásOpciones](https://github.com/MasOpciones)*
