```bash
bash
```

```bash
sudo -i
```

```bash
conda activate mlops
```

```bash
cd root/ApartmentPrice/
```

```bash
sudo systemctl start postgresql
```

```bash
export AIRFLOW_HOME=$PWD/services/airflow
poetry run airflow db init
```

```bash
airflow users create --role Admin --username admin --email admin@example.org --firstname admin --lastname admin --password admin
```

```bash
airflow scheduler --daemon --log-file services/airflow/logs/scheduler.log
airflow webserver --daemon --log-file services/airflow/logs/webserver.log
airflow triggerer --daemon --log-file services/airflow/logs/triggerer.log
```