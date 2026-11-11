# Se ejecuto en un notebook de Databricks (computo serverless) usando el SDK de Databricks.
# Crea el job con sus dos tareas y el pipeline declarativo.
from databricks.sdk import WorkspaceClient
from databricks.sdk.service import jobs, pipelines

w = WorkspaceClient()
carpeta = f"/Users/{w.current_user.me().user_name}/ActividadDatabricks"

# Job con dos tareas: transformar_ventas depende de cargar_ventas
job = w.jobs.create(
    name="job_ventas_pablogilm",
    tasks=[
        jobs.Task(
            task_key="cargar_ventas",
            notebook_task=jobs.NotebookTask(notebook_path=carpeta + "/01_cargar_ventas"),
        ),
        jobs.Task(
            task_key="transformar_ventas",
            depends_on=[jobs.TaskDependency(task_key="cargar_ventas")],
            run_if=jobs.RunIf.ALL_SUCCESS,
            notebook_task=jobs.NotebookTask(notebook_path=carpeta + "/02_transformar_ventas"),
        ),
    ],
)

# Pipeline declarativo (Lakeflow) serverless que publica en workspace.ingenieria_datos_pablogilm
pipe = w.pipelines.create(
    name="pipeline_ventas_pablogilm",
    catalog="workspace",
    schema="ingenieria_datos_pablogilm",
    serverless=True,
    development=True,
    root_path=carpeta + "/pipeline",
    libraries=[pipelines.PipelineLibrary(
        file=pipelines.FileLibrary(path=carpeta + "/pipeline/ventas_pipeline.sql"))],
)

print("Job id:", job.job_id)
print("Pipeline id:", pipe.pipeline_id)
