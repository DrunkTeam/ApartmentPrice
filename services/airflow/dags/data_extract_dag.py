from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import os
import subprocess
import yaml

# import function from phase 1
from src.data import sample_data
from src.validate_data import validate_initial_data

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 7, 30),
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


def increment_version(version):
    """Увеличивает версию на 0.0.1"""
    major, minor, patch = map(int, version.strip('v').split('.'))
    patch += 1
    return f"v{major}.{minor}.{patch}"


def version_data_task(**kwargs):
    config_path = '/home/kama/Documents/MLOps/ApartmentPrice/configs/data_version.yaml'

    # Чтение текущей версии из data_version.yaml
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        # Если файл не найден, начинаем с версии 0.0.0
        config = {'data_version': 'v0.0.0'}

    current_version = config.get('data_version', 'v0.0.0')
    new_version = increment_version(current_version)

    data_path = 'data/samples/sample.csv'
    branch = "dev-kama"

    # Выполнение скрипта test_data.sh с новой версией
    subprocess.run(["bash", "scripts/test_data.sh", data_path, new_version, branch], check=True)

    # Обновление файла с версией данных
    with open(config_path, 'w') as f:
        yaml.dump({'data_version': new_version}, f)

    print(f"Updated version to {new_version}")


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

extract_task >> validate_task >> version_task >> load_task
