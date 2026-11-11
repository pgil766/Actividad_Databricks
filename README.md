# Actividad Databricks

Ingeniería de Datos 2026-2 – Universidad EIA
Pablo Gil Macia

Actividad hecha en Databricks Free Edition con cómputo serverless. Se trabajó con 16 ventas de una tienda de tecnología que incluyen una venta duplicada, una sin producto y una con cantidad negativa. Todo se guardó en el catálogo `workspace`, esquema `ingenieria_datos_pablogilm`.

## Contenido

| Archivo / carpeta | Qué es |
|---|---|
| `Actividad Databricks.pdf` | Enunciado de la actividad. |
| `Actividad_Databricks_Pablo_Gil.docx` | Entrega: respuestas de investigación, resultados y explicaciones. |
| `notebooks/01_cargar_ventas.py` | Crea el esquema y guarda las ventas en la tabla Delta `ventas_bronze`. |
| `notebooks/01b_consultar_ventas.py` | Lee `ventas_bronze` desde otro notebook con el nombre completo, cuenta registros y filtra la categoría Audio. |
| `notebooks/02_transformar_ventas.py` | Quita duplicados, aplica reglas de calidad, calcula `total_venta` y genera `ventas_silver` y `ventas_por_categoria`. |
| `notebooks/03_prueba_pipeline.py` | Consulta el resumen del pipeline, agrega una venta a `ventas_bronze` y vuelve a consultar el resumen. |
| `pipeline/ventas_pipeline.sql` | Pipeline declarativo (Lakeflow) con las vistas materializadas `pipeline_ventas_limpias` y `pipeline_ventas_por_categoria`. |
| `apoyo/crear_job_y_pipeline.py` | Script con el que se creó el job `job_ventas_pablogilm` y el pipeline. |
| `apoyo/error_controlado.py` | Script que introduce y corrige el error controlado del ejercicio 3 (columna `cantidad_vendida`). |
| `capturas/` | Evidencias. El número al inicio del nombre indica el ejercicio (00 = workspace, 01 a 04 = ejercicios). |

Los notebooks están en formato fuente de Databricks (`.py`); se pueden importar al workspace con *Import*.

## Resultados principales

- `ventas_bronze`: 16 registros. Después de la limpieza quedan 13 en `ventas_silver`.
- Ventas por categoría: Computadores 8.500.000, Audio 1.380.000, Accesorios 750.000.
- Job: ejecución exitosa, ejecución fallida por el error controlado (la segunda tarea quedó en *Upstream failed*) y ejecución final exitosa.
- Pipeline: al agregar una venta de 480.000 en Audio, el resumen pasó de 1.380.000 a 1.860.000.
