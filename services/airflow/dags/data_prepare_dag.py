from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.sensors.external_task_sensor import ExternalTaskSensor
from airflow.utils.state import DagRunState

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'data_prepare_dag',
    default_args=default_args,
    description='Run ZenML pipeline after data extraction pipeline',
    schedule_interval=timedelta(minutes=5),
    start_date=datetime(2024, 7, 30),
    catchup=False,
)

wait_for_data_extraction = ExternalTaskSensor(
    task_id='wait_for_data_extraction',
    external_dag_id='data_extract_dag',
    external_task_id=None,  # Wait for the entire DAG to complete
    allowed_states=[DagRunState.SUCCESS],
    failed_states=[DagRunState.FAILED],
    mode='poke',
    poke_interval=60,
    timeout=3600,
    dag=dag,
)

run_zenml_pipeline = BashOperator(
    task_id='run_zenml_pipeline',
    bash_command='python /home/kama/Documents/MLOps/ApartmentPrice/services/airflow/dags/data_prepare.py',
    dag=dag,
)

wait_for_data_extraction >> run_zenml_pipeline
