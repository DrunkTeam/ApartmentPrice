# Desciption of files
- app.py - start UI demo of project
- data.py:
    1. init_hydra(config_path="../configs", config_name="main.yaml") -> DictConfig
    Initializes Hydra with the specified configuration file.
    2. download_dataset()
    Downloads and unzips a dataset from Kaggle using the configuration specified in sample_data.yaml.
    3. sample_data(cfg=cfg)
    Samples the dataset according to the configuration in sample_data.yaml, saves the sample, stages it with DVC, and pushes the changes.
    4. clean_string(text)
    Cleans a string by removing carriage returns, newlines, and excess whitespace.
    5. clean_rn(address)
    Cleans an address string by replacing carriage returns and newlines with spaces.
    6. clean_description(description)
    Cleans a description string by removing carriage returns, newlines, and excess whitespace.
    7. remove_numbers(text)
    Removes numbers from a string.
    8. tokenize(address)
    Splits an address into number and letter components.
    9. split_vectors(df, column)
    Splits a DataFrame column containing vectors into separate columns.
    10. read_datastore()
    Reads the sample dataset from DVC and returns it as a DataFrame along with the dataset version.
    11. preprocess_data(df)
    Preprocesses the dataset according to the configuration in ApartmentPrice.yaml. This includes cleaning text, imputing missing values, encoding features, and scaling numerical features.
    12. validate_features(X, y)
    Validates the features using Great Expectations.
    13. load_features(X, y, version)
    Saves the features and target to ZenML and retrieves the latest version if available.

- evaluate.py - evaluate models
  ```bash
  src/evaluate --model-name decision_tree_regressor --model-alias champion --data-version 1
  ```
- main.py - file for running mlflow
- model.py - script for training and plotting artifacts in mlflow
- models.py - code of the NN models with wrapper
- predict.py - artifact for testing of post request
- reproducing.py - calculate reproducibility of model from main.yaml
- transform.py - call dag of prepare_data_pipeline
- validate.py - script to find the champion from models
- validate_after_preproc.py - function to validate data after preprocessing
- validate_data.py - function to validate data after downloading
