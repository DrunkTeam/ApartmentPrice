# Airflow dags (files from services/airflow/dags)

## Running
### Change paths
```bash
cd services/airflow/
```

```bash
nano airflow.cfg
```

Changed paths to yours path: 
dags_folder = {your_path}/ApartmentPrice/services/airflow/dags
plugins_folder = {your_path}/ApartmentPrice/services/airflow/plugins
base_log_folder = {your_path}/ApartmentPrice/services/airflow/logs
dag_processor_manager_log_location = {your_path}/ApartmentPrice/services/airflow/logs/dag_processor_manager/dag_processor_man>
config_file = {your_path}/ApartmentPrice/services/airflow/webserver_config.py
child_process_log_directory = {your_path}/ApartmentPrice/services/airflow/logs/scheduler

### Create database for our data
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

1. Open this file
```bash
sudo nano /etc/postgresql/16/main/pg_hba.conf
```

2. Add the following line to the end of this file
host all all 0.0.0.0/0 trust

3. Save the change and close it

4. Open another file
```bash
sudo nano /etc/postgresql/16/main/postgresql.conf
```

5. Add the line as follows
```
#------------------------------------------------------------------------------
# CONNECTIONS AND AUTHENTICATION
#------------------------------------------------------------------------------

# - Connection Settings -

listen_addresses = '*'
```

6. Save the change and close it

```bash
sudo systemctl restart postgresql
```

### Run airflow services

```bash
export AIRFLOW_HOME=$PWD/services/airflow
poetry run airflow db init
```

```bash
airflow users create --role Admin --username admin --email admin@example.org --firstname admin --lastname admin --password admin
```

```bash
export PYTHONPATH=$PWD/src
echo "export PYTHONPATH=$PWD/src" >> ~/.bashrc
source ~/.bashrc
conda activate mlops
mkdir -p $AIRFLOW_HOME/logs $AIRFLOW_HOME/dags
echo > $AIRFLOW_HOME/logs/scheduler.log
echo > $AIRFLOW_HOME/logs/triggerer.log
echo > $AIRFLOW_HOME/logs/webserver.log
echo *.log >> $AIRFLOW_HOME/logs/.gitignore
```

```bash
airflow scheduler --daemon --log-file services/airflow/logs/scheduler.log
airflow webserver --daemon --log-file services/airflow/logs/webserver.log
airflow triggerer --daemon --log-file services/airflow/logs/triggerer.log
```
