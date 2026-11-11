# Databricks notebook source
# MAGIC %md
# MAGIC # 01 - Cargar ventas
# MAGIC Crea el esquema del curso y guarda las ventas de la tienda como tabla Delta (`ventas_bronze`).
# MAGIC
# MAGIC Los datos traen errores a propósito: una venta duplicada (id 3), una venta sin producto (id 14) y una venta con cantidad negativa (id 15).

# COMMAND ----------

from datetime import date
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DateType, DoubleType

CATALOGO = "workspace"
ESQUEMA = "ingenieria_datos_pablogilm"
TABLA_BRONZE = f"{CATALOGO}.{ESQUEMA}.ventas_bronze"

spark.sql(f"CREATE SCHEMA IF NOT EXISTS {CATALOGO}.{ESQUEMA}")

# COMMAND ----------

esquema_ventas = StructType([
    StructField("id_venta", IntegerType(), False),
    StructField("fecha", DateType(), True),
    StructField("producto", StringType(), True),
    StructField("categoria", StringType(), True),
    StructField("cantidad", IntegerType(), True),
    StructField("precio_unitario", DoubleType(), True),
])

ventas = [
    (1,  date(2026, 10, 1), "Portatil Lenovo IdeaPad 3",   "Computadores", 1, 2800000.0),
    (2,  date(2026, 10, 1), "Mouse Logitech M170",         "Accesorios",   3, 45000.0),
    (3,  date(2026, 10, 2), "Audifonos Sony WH-CH520",     "Audio",        2, 230000.0),
    (4,  date(2026, 10, 2), "Teclado mecanico Redragon",   "Accesorios",   1, 180000.0),
    (5,  date(2026, 10, 3), "Monitor Samsung 24",          "Computadores", 2, 650000.0),
    (6,  date(2026, 10, 3), "Parlante JBL Go 3",           "Audio",        1, 190000.0),
    (7,  date(2026, 10, 4), "Base refrigerante portatil",  "Accesorios",   2, 85000.0),
    (8,  date(2026, 10, 4), "Portatil HP 15",              "Computadores", 1, 2500000.0),
    (9,  date(2026, 10, 5), "Audifonos JBL Tune 510",      "Audio",        1, 210000.0),
    (10, date(2026, 10, 5), "Memoria USB 64GB",            "Accesorios",   4, 35000.0),
    (11, date(2026, 10, 6), "Barra de sonido LG",          "Audio",        1, 520000.0),
    (12, date(2026, 10, 6), "Mini PC Intel NUC",           "Computadores", 1, 1900000.0),
    (13, date(2026, 10, 7), "Cable HDMI 2m",               "Accesorios",   5, 25000.0),
    (14, date(2026, 10, 7), None,                          "Audio",        2, 150000.0),   # venta sin producto
    (15, date(2026, 10, 8), "Mouse inalambrico",           "Accesorios",  -2, 60000.0),    # cantidad negativa
    (3,  date(2026, 10, 2), "Audifonos Sony WH-CH520",     "Audio",        2, 230000.0),   # venta duplicada
]

df_ventas = spark.createDataFrame(ventas, esquema_ventas)
df_ventas = df_ventas.select("id_venta", "fecha", "producto", "categoria", "cantidad", "precio_unitario")
display(df_ventas)

# COMMAND ----------

# Se usa overwrite para que volver a correr el notebook no duplique la carga
(df_ventas.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable(TABLA_BRONZE))

print(f"Tabla {TABLA_BRONZE} guardada con {spark.table(TABLA_BRONZE).count()} registros")
