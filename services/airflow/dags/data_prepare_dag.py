import os
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.sensors.external_task_sensor import ExternalTaskSensor
from datetime import datetime, timedelta, date

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 7, 30),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'data_prepare_dag',
    default_args=default_args,
    description='DAG for data preparation',
    schedule_interval=timedelta(minutes=5),
)

wait_for_data_extraction = ExternalTaskSensor(
    task_id='wait_for_data_extraction',
    external_dag_id='data_extract_dag',
    external_task_id=None,
    check_existence=True,
    timeout=600,
    mode='poke',
    poke_interval=60,
    dag=dag,
)

run_zenml_pipeline = BashOperator(
    task_id='run_zenml_pipeline',
    bash_command='zenml pipeline run',
    dag=dag,
)

load_features_to_store = BashOperator(
    task_id='load_features_to_store',
    bash_command='feast -c services/feast/feast_project/feature_repo apply',
    dag=dag,
)

wait_for_data_extraction >> run_zenml_pipeline >> load_features_to_store