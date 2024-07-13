<<<<<<< HEAD:start.md
=======
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
cd /root/ApartmentPrice/
```

```bash
sudo systemctl start postgresql
sudo -u postgres psql
```

```bash
CREATE USER ninel WITH PASSWORD 'ninel';
CREATE DATABASE airflow;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO ninel;
show hba_file;
\q
```

```bash
sudo systemctl restart postgresql
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
airflow triggerer --daemon --log-file services/airflow/logs/triggerer.log
```

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

Чтобы оставить сессию tmux без закрытия после завершения SSH-соединения, нажмите Ctrl+b, затем d (отделение от сессии).

При следующем подключении через SSH можно будет вернуться к сессии tmux:

```bash
tmux attach -t airflow_session
```
>>>>>>> 33d3dabb81455c417ff5214a76453f6a52852f82:airflow_start.md
