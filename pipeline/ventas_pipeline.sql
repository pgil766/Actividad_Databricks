-- Pipeline declarativo de ventas (Lakeflow Spark Declarative Pipelines)
-- Fuente: workspace.ingenieria_datos_pablogilm.ventas_bronze

CREATE OR REFRESH MATERIALIZED VIEW pipeline_ventas_limpias
COMMENT "Ventas sin duplicados, con producto, cantidad y precio validos"
AS
SELECT DISTINCT
  id_venta,
  fecha,
  producto,
  categoria,
  cantidad,
  precio_unitario,
  cantidad * precio_unitario AS total_venta
FROM workspace.ingenieria_datos_pablogilm.ventas_bronze
WHERE producto IS NOT NULL
  AND TRIM(producto) <> ''
  AND cantidad > 0
  AND precio_unitario > 0;

CREATE OR REFRESH MATERIALIZED VIEW pipeline_ventas_por_categoria
COMMENT "Valor total vendido por categoria"
AS
SELECT
  categoria,
  SUM(total_venta) AS total_vendido,
  COUNT(*) AS numero_ventas
FROM pipeline_ventas_limpias
GROUP BY categoria;
