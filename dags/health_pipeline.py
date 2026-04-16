from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 1, 1),
}

with DAG(
    "health_pipeline",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False
) as dag:

    ingest = BashOperator(
        task_id="ingest_data",
        bash_command="python /opt/airflow/project/pipelines/ingest.py"
    )

    transform = BashOperator(
        task_id="transform_data",
        bash_command="python /opt/airflow/project/pipelines/transform.py"
    )

    train = BashOperator(
        task_id="train_model",
        bash_command="python /opt/airflow/project/models/model.py"
    )

    ingest >> transform >> train