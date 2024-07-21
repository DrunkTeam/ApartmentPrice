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
cd /home/kama/Documents/MLOps/ApartmentPrice/
```

```bash
sudo systemctl start postgresql
sudo -u postgres psql
```

```bash
CREATE USER ninel WITH PASSWORD 'ninel';
CREATE ROLE ninel WITH LOGIN PASSWORD 'ninel';
ALTER ROLE ninel WITH SUPERUSER;
CREATE DATABASE airflow;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO ninel;
GRANT ALL PRIVILEGES ON DATABASE airflow TO ninel;
show hba_file;
\q
```

```bash
sudo systemctl restart postgresql
```

```bash
export AIRFLOW_HOME=$PWD/services/airflow
export AIRFLOW__CORE__DAGS_FOLDER=$PWD/services/airflow/dags
export PYTHONPATH=$PYTHONPATH:$PWD
poetry run airflow db init
```

```bash
airflow users create --role Admin --username admin --email admin@example.org --firstname admin --lastname admin --password admin
```

```bash
airflow scheduler --log-file services/airflow/logs/scheduler.log
airflow triggerer --log-file services/airflow/logs/triggerer.log
airflow webserver --log-file services/airflow/logs/webserver.log
```

If you want to kill all Airflow processes/daemons in the background, run as follows:
```bash
kill $(ps -ef | grep "airflow" | awk '{print $2}')
```

```bash
sudo lsof -i :8793
sudo lsof -i :8794
```

Это больше не нужно

```bash
tmux kill-session -t airflow_session
```

```bash
tmux new -s airflow_session
```

```bash
conda activate mlops
```

```bash
airflow webserver --log-file services/airflow/logs/webserver.log
```

На случай, если потребуется убить процесс airflow webserver. после убийства, надо запустить заново строчку выше
```bash
sudo kill -9 (PID)
```

Чтобы оставить сессию tmux без закрытия после завершения SSH-соединения, нажмите Ctrl+b, затем d (отделение от сессии).

При следующем подключении через SSH можно будет вернуться к сессии tmux:

```bash
tmux attach -t airflow_session
```