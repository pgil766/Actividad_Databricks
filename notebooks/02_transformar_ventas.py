# Databricks notebook source
# MAGIC %md
# MAGIC # 02 - Transformar ventas
# MAGIC Limpia `ventas_bronze`, calcula el total de cada venta y genera las tablas `ventas_silver` y `ventas_por_categoria`.

# COMMAND ----------

from pyspark.sql import functions as F

CATALOGO = "workspace"
ESQUEMA = "ingenieria_datos_pablogilm"
TABLA_BRONZE = f"{CATALOGO}.{ESQUEMA}.ventas_bronze"
TABLA_SILVER = f"{CATALOGO}.{ESQUEMA}.ventas_silver"
TABLA_CATEGORIA = f"{CATALOGO}.{ESQUEMA}.ventas_por_categoria"

bronze = spark.table(TABLA_BRONZE)
registros_bronze = bronze.count()

# COMMAND ----------

# 1. Quitar registros identicos duplicados
sin_duplicados = bronze.dropDuplicates()
registros_sin_duplicados = sin_duplicados.count()

# 2. Reglas de calidad: producto presente, cantidad > 0 y precio_unitario > 0
ventas_limpias = (sin_duplicados
    .filter(F.col("producto").isNotNull() & (F.trim(F.col("producto")) != ""))
    .filter(F.col("cantidad") > 0)
    .filter(F.col("precio_unitario") > 0)
    .withColumn("total_venta", F.col("cantidad") * F.col("precio_unitario")))

registros_silver = ventas_limpias.count()

print(f"Registros en bronze:            {registros_bronze}")
print(f"Despues de quitar duplicados:   {registros_sin_duplicados}")
print(f"Despues de reglas de calidad:   {registros_silver}")

# COMMAND ----------

# overwrite: si el notebook se ejecuta otra vez la tabla se reemplaza y no se acumulan registros
(ventas_limpias.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable(TABLA_SILVER))

display(spark.table(TABLA_SILVER).orderBy("id_venta"))

# COMMAND ----------

ventas_por_categoria = (spark.table(TABLA_SILVER)
    .groupBy("categoria")
    .agg(F.sum("total_venta").alias("total_vendido"),
         F.count("*").alias("numero_ventas"))
    .orderBy(F.desc("total_vendido")))

(ventas_por_categoria.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable(TABLA_CATEGORIA))

display(spark.table(TABLA_CATEGORIA))

# COMMAND ----------

# Verificacion de que no se acumulan registros al repetir el proceso
silver = spark.table(TABLA_SILVER)
ids_repetidos = silver.groupBy("id_venta").count().filter("count > 1").count()

print(f"Registros en ventas_silver:         {silver.count()}")
print(f"Registros en ventas_por_categoria:  {spark.table(TABLA_CATEGORIA).count()}")
print(f"id_venta repetidos en silver:       {ids_repetidos}")
