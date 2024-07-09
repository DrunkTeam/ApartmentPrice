# Последовательности текущих действий для поднятия проекта на серваке Ubuntu
```bash
ssh kama@91.224.86.145
```

```bash
sudo -i
```

```bash
sudo apt update
sudo apt upgrade
```

```bash
sudo apt install python3.11
sudo apt install python3.11-venv
```

```bash
wget https://repo.anaconda.com/archive/Anaconda3-2024.06-1-Linux-x86_64.sh
```

```bash
bash Anaconda3-2024.06-1-Linux-x86_64.sh
```
Anaconda3 will now be installed into this location:
/root/anaconda3
PREFIX=/root/anaconda3

installation finished.
Do you wish to update your shell profile to automatically initialize conda?
This will activate conda on startup and change the command prompt when activated.
If you'd prefer that conda's base environment not be activated on startup,
   run the following command when conda is activated:

conda config --set auto_activate_base false

You can undo this by running `conda init --reverse $SHELL`? [yes|no]

[no] >>> yes
no change     /root/anaconda3/condabin/conda
no change     /root/anaconda3/bin/conda
no change     /root/anaconda3/bin/conda-env
no change     /root/anaconda3/bin/activate
no change     /root/anaconda3/bin/deactivate
no change     /root/anaconda3/etc/profile.d/conda.sh
no change     /root/anaconda3/etc/fish/conf.d/conda.fish
no change     /root/anaconda3/shell/condabin/Conda.psm1
no change     /root/anaconda3/shell/condabin/conda-hook.ps1
no change     /root/anaconda3/lib/python3.12/site-packages/xontrib/conda.xsh
no change     /root/anaconda3/etc/profile.d/conda.csh
modified      /root/.bashrc

==> For changes to take effect, close and re-open your current shell. <==

Thank you for installing Anaconda3!

```bash
sudo apt-get install postgresql
```

```bash
sudo systemctl start postgresql
```

```bash
exit
```

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

```bash
sudo -i
```

```bash
conda create -n mlops python=3.11.0
```

```bash
conda activate mlops
```

```bash
pip install poetry==1.8.1
```

```bash
poetry install
```

```bash
exit
```

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

```bash
echo; echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"'
```

```bash
eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"
```

```bash
sudo apt-get install build-essential
```

```bash
mkdir ~/ApartmentPrice
```

```bash
cd ~/ApartmentPrice
```

```bash
git clone https://github.com/DrunkTeam/ApartmentPrice.git .
```

```bash
git checkout dev-kama
```

```bash
pip install poetry==1.8.1
```

```bash
poetry install
```

Current Python version (3.11.0) is not allowed by the project (3.10.13).
Please change python executable via the "env use" command.

Из-за этой ошибки надо поменять в файле poetry.lock поменять в последней строчке версию python с 3.10.13 на 3.11.0

```bash
git pull
```

Ошибка не ушла, но мы пошли дальше

```bash
cd /root/ApartmentPrice/services/airflow/
```

```bash
nano airflow.cfg
```

Меняем пути на 
dags_folder = /root/ApartmentPrice/services/airflow/dags
plugins_folder = /root/ApartmentPrice/services/airflow/plugins
base_log_folder = /root/ApartmentPrice/services/airflow/logs
dag_processor_manager_log_location = /root/ApartmentPrice/services/airflow/logs/dag_processor_manager/dag_processor_man>
config_file = /root/ApartmentPrice/services/airflow/webserver_config.py
child_process_log_directory = /root/ApartmentPrice/services/airflow/logs/scheduler

```bash
cd /root/ApartmentPrice/services/airflow
```

```bash
mkdir dags
```

```bash
poetry lock --no-update
```

```bash
poetry install
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
sudo nano /etc/postgresql/14/main/pg_hba.conf
```

# 1. Open this file
sudo nano /etc/postgresql/14/main/pg_hba.conf

# 2. Add the following line to the end of this file
host all all 0.0.0.0/0 trust

# 3. Save the change and close it

# 4. Open another file
sudo nano /etc/postgresql/14/main/postgresql.conf

# 5. Add the line as follows

#------------------------------------------------------------------------------
# CONNECTIONS AND AUTHENTICATION
#------------------------------------------------------------------------------

# - Connection Settings -

listen_addresses = '*'

# 6. Save the change and close it

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
