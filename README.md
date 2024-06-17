# ApartmentPrice
For Equity Residential, the challenge lies in accurately adjusting rental prices for their apartments on a daily basis to maximize revenue while maintaining competitive occupancy rates.

## The structure of repo
├───README.md          # Repo docs \
├───.gitignore         # gitignore file \
├───requirements.txt   # Python packages   \
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
├───sql                # SQL files \
├───src                # Python scripts \
└───tests              # Scripts for testing Python code \

##Installing
To install environments and requirements, use the following script:
```bash
./scripts/install_requirements.sh
```