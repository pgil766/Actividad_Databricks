MODO = "error"   # "error" para introducir el fallo, "corregir" para quitarlo

import base64
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.workspace import ImportFormat, Language, ExportFormat
w = WorkspaceClient()
ruta = f"/Users/{w.current_user.me().user_name}/ActividadDatabricks/01_cargar_ventas"
src = base64.b64decode(w.workspace.export(ruta, format=ExportFormat.SOURCE).content).decode()
bien = '"cantidad", "precio_unitario")'
mal = '"cantidad_vendida", "precio_unitario")'
nuevo = src.replace(bien, mal) if MODO == "error" else src.replace(mal, bien)
w.workspace.import_(ruta, content=base64.b64encode(nuevo.encode()).decode(), format=ImportFormat.SOURCE, language=Language.PYTHON, overwrite=True)
print("Modo:", MODO, "| cambio aplicado:", nuevo != src)
