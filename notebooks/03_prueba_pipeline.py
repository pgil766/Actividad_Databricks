# Databricks notebook source
# MAGIC %md
# MAGIC # 03 - Prueba del pipeline
# MAGIC Se consulta el resumen del pipeline, se agrega una venta valida a `ventas_bronze` y, despues de volver a ejecutar el pipeline, se compara el resultado.
# MAGIC No se ejecuta el notebook de carga durante esta prueba.

# COMMAND ----------

# MAGIC %sql
# MAGIC -- ANTES: resumen generado por el pipeline
# MAGIC SELECT categoria, total_vendido, numero_ventas
# MAGIC FROM workspace.ingenieria_datos_pablogilm.pipeline_ventas_por_categoria
# MAGIC ORDER BY total_vendido DESC

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Se agrega una venta valida: 1 parlante de 480.000 en la categoria Audio
# MAGIC INSERT INTO workspace.ingenieria_datos_pablogilm.ventas_bronze
# MAGIC VALUES (17, DATE'2026-10-09', 'Parlante JBL Flip 6', 'Audio', 1, 480000.0)

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) AS registros_bronze
# MAGIC FROM workspace.ingenieria_datos_pablogilm.ventas_bronze

# COMMAND ----------

# MAGIC %md
# MAGIC Ahora se vuelve a ejecutar el pipeline desde Jobs & Pipelines y luego se corre la siguiente celda.

# COMMAND ----------

# MAGIC %sql
# MAGIC -- DESPUES: resumen del pipeline luego de la nueva ejecucion
# MAGIC SELECT categoria, total_vendido, numero_ventas
# MAGIC FROM workspace.ingenieria_datos_pablogilm.pipeline_ventas_por_categoria
# MAGIC ORDER BY total_vendido DESC
