from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import os
import subprocess
import yaml

# Импортируем функции из фазы 1
from src.data import sample_data
from src.validate_data import validate_initial_data

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 7, 19),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'data_extract_dag',
    default_args=default_args,
    description='DAG for data extraction, validation, versioning, and loading',
    schedule_interval=timedelta(minutes=5),
)


def extract_data_task(**kwargs):
    sample_data()


def validate_data_task(**kwargs):
    validate_initial_data(csv_path='data/samples/sample.csv')


def version_data_task(**kwargs):
    data_path = 'data/samples/sample.csv'
    tag_name = "v1.0.0"
    branch = "main"

    # Выполнение скрипта test_data.sh
    subprocess.run(["bash", "scripts/test_data.sh", data_path, tag_name, branch], check=True)

    # Обновление файла с версией данных
    version = tag_name
    config_path = './configs/data_version.yaml'
    with open(config_path, 'w') as f:
        yaml.dump({'data_version': version}, f)


def load_data_task(**kwargs):
    # Используем DVC для загрузки данных в удаленное хранилище
    os.system('dvc push')


extract_task = PythonOperator(
    task_id='extract_data',
    python_callable=extract_data_task,
    dag=dag,
)

validate_task = PythonOperator(
    task_id='validate_data',
    python_callable=validate_data_task,
    dag=dag,
)

version_task = PythonOperator(
    task_id='version_data',
    python_callable=version_data_task,
    dag=dag,
)

load_task = PythonOperator(
    task_id='load_data',
    python_callable=load_data_task,
    dag=dag,
)

if __name__ == '__main__':
    print("It work")
    extract_task >> validate_task >> version_task >> load_task
