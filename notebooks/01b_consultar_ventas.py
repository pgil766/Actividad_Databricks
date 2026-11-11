# Databricks notebook source
# MAGIC %md
# MAGIC # 01b - Consultar ventas
# MAGIC Lee la tabla `ventas_bronze` desde otro notebook usando el nombre completo `catalogo.esquema.tabla`.

# COMMAND ----------

ventas = spark.table("workspace.ingenieria_datos_pablogilm.ventas_bronze")
ventas.printSchema()
display(ventas)

# COMMAND ----------

print("Cantidad de registros:", ventas.count())

# COMMAND ----------

# Ventas de la categoria Audio
display(ventas.filter(ventas.categoria == "Audio").orderBy("id_venta"))

# COMMAND ----------

# MAGIC %sql
# MAGIC -- La misma consulta en SQL
# MAGIC SELECT COUNT(*) AS total_registros
# MAGIC FROM workspace.ingenieria_datos_pablogilm.ventas_bronze
