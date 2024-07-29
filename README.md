![Test code workflow](https://github.com/DrunkTeam/ApartmentPrice/actions/workflows/test-code.yaml/badge.svg)
![Validate model workflow](https://github.com/Palandr123/MLOps-Project/actions/workflows/validate-model.yaml/badge.svg)
# ApartmentPrice
For Equity Residential, the challenge lies in accurately adjusting rental prices for their apartments on a daily basis to maximize revenue while maintaining competitive occupancy rates.

## The structure of repo
```
├───README.md          # Repo docs \
├───.gitignore         # gitignore file \
├───configs            # Hydra configuration management \
├───data               # All data \
├───docs               # Project docs like reports or figures \
├───models             # ML models \
├───notebooks          # Jupyter notebooks \
├───outputs            # Outputs of Hydra \
├───pipelines          # A Soft link to DAGs of Apache Airflow \
├───reports            # Generated reports \
├───scripts            # Shell scripts (.sh) \
├───services           # Metadata of services (PostgreSQL, Feast, Apache airflow, ...etc) \
├───src                # Python scripts \
└───tests              # Scripts for testing Python code \
```

## Installing
To install environments and requirements, use the following script:
```bash
conda create -n mlops python=3.11.9 
conda activate mlops
pip install poetry==1.8.1
poetry install

poetry run ... write command (example, python src/data.py)
```

## Deployment Instructions
Launch Docker Container:

```bash
docker run -d -p 5152:8080 --name team_6_ml_service
```
Start Flask API:

```bash
python api/app.py
```

Initiate Gradio UI:

```bash
python src/app.py
```

## Running
You can run many elemnts of our project: from airflow to CI/CD. Instructions you can find in relevant folders and in folder 'docs'

## Listening ports
MLflow: 5000 \
ZenML: 8237 \
Flask: 5001 \
UI: 5155 \
Airflow:
  - scheduler : 8793
  - triger : 8794
  - webserver: 8882 

