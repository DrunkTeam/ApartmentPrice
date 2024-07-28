import os
import sys
current_directory = os.getcwd()
sys.path.append(current_directory)
from services.airflow.dags.data_prepare import prepare_data_pipeline

def main():
    print("Testing zenml pipeline")
    prepare_data_pipeline()
    print("Zenml pipeline successfully completed!")


if __name__ == "__main__":
    main()