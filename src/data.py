import os
import dvc.api
import pandas as pd
import zenml
import numpy as np
import great_expectations as gx
import dvc.api
import datetime as dt
import re
from subprocess import run
from zipfile import ZipFile

from omegaconf import DictConfig
from hydra.core.global_hydra import GlobalHydra
from hydra import compose, initialize
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from gensim.models import Word2Vec
from gensim.utils import simple_preprocess
from pathlib import Path
from zenml.client import Client




def init_hydra(config_path="../configs", config_name="main.yaml") -> DictConfig:
    """
    Initializes hydra
    """

    if GlobalHydra.instance().is_initialized():
        GlobalHydra.instance().clear()

    initialize(config_path=config_path, version_base=None)
    cfg = compose(config_name)

    return cfg


cfg = init_hydra()

def download_dataset():

    cfg = compose(config_name="sample_data")

    #  #Define the dataset path
    # dataset_path = Path(cfg.path)
    # dataset_path.parent.mkdir(parents=True, exist_ok=True)

    # # Check if the dataset already exists
    # if not dataset_path.exists():
    #     try:
    #         # Run the kaggle command to download the dataset using poetry
    #         run(
    #             [
    #                 "poetry",
    #                 "run",
    #                 "kaggle",
    #                 "datasets",
    #                 "download",
    #                 f"{cfg.user_name}/{cfg.dataset_name}",
    #             ],
    #             check=True,
    #         )

    #         # Extract the contents of the downloaded zip file
    #         with ZipFile(f"{cfg.dataset_name}.zip", 'r') as zip_ref:
    #             zip_ref.extractall(dataset_path.parent)

    #         # Find and rename the extracted CSV file to the target path
    #         extracted_files = list(dataset_path.parent.glob("*.csv"))
    #         if extracted_files:
    #             extracted_files[0].rename(dataset_path)

    #         # Remove the zip file after extraction
    #         os.remove(f"{cfg.dataset_name}.zip")

    #     except subprocess.CalledProcessError as e:
    #         print(f"Error occurred while downloading the dataset: {e}")

    # else:
    #     print(f"Dataset already exists at {dataset_path}")

    data_path = Path(cfg.path)
    data_path.parent.mkdir(exist_ok=True, parents=True)
    if not data_path.exists():
        run(
            [
                "poetry",
                "run",
                "kaggle",
                "datasets",
                "download",
                f"{cfg.user_name}/{cfg.dataset_name}",
            ],
            check=True,
        )
        with ZipFile(f"{cfg.dataset_name}.zip", 'r') as zip_file:
            # Assuming there's only one CSV file in the archive
            csv_file = zip_file.namelist()[0]
            zip_file.extract(csv_file, data_path.parent)
            (data_path.parent / csv_file).rename(data_path)
        os.remove(Path(f"{cfg.dataset_name}.zip"))

    else:
        print(f"Data already exists: {data_path}")


# @hydra.main(config_path="../configs", config_name = "main", version_base=None)
def sample_data(cfg=cfg):
    cfg = compose(config_name="sample_data")

    download_dataset()
    data_url = dvc.api.get_url(
        path=cfg.data.path,
        remote=cfg.data.remote,
        repo=cfg.data.repo,
        rev=cfg.data.version
    )
    sample_size = cfg.data.sample_size

    # Take a sample of the data
    data = pd.read_csv(data_url)
    sample = data.sample(frac=sample_size, random_state=cfg.data.random_state)

    os.makedirs('data/samples', exist_ok=True)
    sample.to_csv('data/samples/sample.csv', index=False)

    # Stage the sample data file for DVC and push the changes with DVC
    os.system('dvc add data/samples/sample.csv')
    os.system('dvc push')


def clean_string(text):
    if isinstance(text, str):
        cleaned_text = re.sub(r'[\r\n]+', '', text)
        cleaned_text = re.sub(r'\s+', '', cleaned_text.strip())
        return cleaned_text
    else:
        return text


def clean_rn(address):
    # Check if the address is a string
    if isinstance(address, str):
        cleaned_address = address.replace('\r\n', ' ').replace('\n', ' ').replace('\r', ' ')
        cleaned_address = ' '.join(cleaned_address.split())
        return cleaned_address
    else:
        # Return the address as is if it's not a string
        return address


def clean_description(description):
    if isinstance(description, str):
        cleaned_string = re.sub(r'[\r\n]+', ' ', description).strip()
        return cleaned_string
    else:
        return description


def remove_numbers(text):
    if isinstance(text, str):
        return re.sub(r'\s+', ' ', text).strip()
    return text


def tokenize(address):
    match = re.match(r"(\d+)([a-zA-Z]+)", address)
    if match:
        return [match.group(1), match.group(2)]
    return [address]


def split_vectors(df, column):
    vector_df = pd.DataFrame(df[column].tolist(), index=df.index)
    vector_df.columns = [f'{column}_{i}' for i in range(vector_df.shape[1])]
    return vector_df


def read_datastore():
    """
    Read sample and return in dataframe format to ZenML pipeline

    """
    # Initialize Hydra with config path (replace with your config file)
    # we have to read them from the datastore after the 1 task in this phase
    # initialize(config_path="../configs", version_base="1.1")
    # cfg = compose(config_name="data_version")
    # version_num = cfg.data_version

    # sample_path = Path("data") / "samples" / "sample.csv"
    # df = pd.read_csv(sample_path)
    # return df, version_num
    # relative_path = os.path.join('data', 'samples', cfg.data.sample_filename)
    # path=Path("data")
    data_url = dvc.api.get_url(
        path=cfg.data.path,
        remote=cfg.data.remote,
        repo=cfg.data.repo,
        rev=str(cfg.data.version)
    )
    version_num = str(cfg.data.version)

    # Take a sample of the data
    df = pd.read_csv(data_url)

    return df, version_num


# all columns name should be in the configs
# small function should be separate from the function 'preprocess_data'

def preprocess_data(df):
    """
    Preprocess data step in ZenML pipeline

    """
    # client = zenml.client.Client()
    # initialize(config_path="../configs/data", version_base="1.1")
    cfg = compose(config_name="ApartmentPrice")

    # column contains just index of the row
    df.drop('Unnamed: 0', axis=1, inplace=True)

    # Columns which dublicate the information from different text columns
    # dublicate_cols = ['unit_id','Apartment Name', 'URL','building_id']
    dublicate_cols = cfg.dublicate_cols
    df = df.drop(dublicate_cols, axis=1)

    # Remove unnecessary characters from remaining text features

    clean_rn_col = cfg.clean_rn_columns

    df[clean_rn_col] = df[clean_rn_col].apply(clean_rn).str.lower()

    clean_description_col = cfg.clean_description_columns

    df[clean_description_col] = df[clean_description_col].apply(clean_description).str.lower()

    # clean excess spaces
    df[clean_description_col] = df[clean_description_col].astype(str)
    df[clean_description_col] = df[clean_description_col].apply(remove_numbers)

    clean_string_col = cfg.clean_string_columns

    df[clean_string_col] = df[clean_string_col].apply(clean_string).str.lower()

    # Impute missing values with 'most-frequent' strategy

    imp_most_frequent = SimpleImputer(missing_values=np.nan, strategy='most_frequent')


    cols_most_frequent = cfg.columns_most_frequent
    for i in cols_most_frequent:
        df[[i]] = imp_most_frequent.fit_transform(df[[i]])


    df[clean_string_col] = df[clean_string_col].fillna(df[clean_string_col].mode()[0])




    New_date = []

    todatetime_col = cfg.todatatime_columns

    for feature in [todatetime_col]:
        df[feature] = pd.to_datetime(df[feature])

    for i in range(df.shape[0]):
        Move_date = df[todatetime_col].iloc[i] + dt.timedelta(days=df[cfg.col_for_imputing_date][i])
        New_date.append(Move_date)

    df[cfg.col_for_new_date] = pd.to_datetime(New_date)

    df.drop(cfg.col_for_old_date, axis=1, inplace=True)

    # Sorted data by 'Day_Recorded' like time series
    df.sort_values(by=todatetime_col, inplace=True)

    # Transform date to month, day to further transform

    df["Move_in_date_day"] = df[cfg.col_for_new_date].dt.day
    df["Move_in_date_month"] = df[cfg.col_for_new_date].dt.month
    df["Move_in_date_year"] = df[cfg.col_for_new_date].dt.year

    df.drop([cfg.col_for_new_date, cfg.todatatime_columns, "Move_in_date_year"], axis=1, inplace=True)

    # One-hot encoding
    ohe_col = cfg.ohe_columns
    cities = pd.get_dummies(df[ohe_col], dtype=float).drop(df[ohe_col].value_counts().tail(1).index[0], axis=1)
    df = pd.concat([df, cities], axis=1)
    df.drop([ohe_col], axis=1, inplace=True)

    # Label encoding
    # label_encoding = {'Tuesday': 1, 'Saturday': 2,'Friday': 3, 'Sunday': 4, 'Monday': 5, 'Wednesday': 6, 'Thursday': 7}
    df[cfg.columns_for_label_enc] = df[cfg.columns_for_label_enc].apply(lambda x: cfg.label_encoding.get(x))

    # Encoding text features using embeddings
    # Text preprocessing
    df['clean_description_col_processed'] = df[clean_description_col].apply(lambda x: simple_preprocess(x))
    # Learning the Word2Vec model
    model_Amenity = Word2Vec(sentences=df['clean_description_col_processed'], vector_size=10, window=5, min_count=1,
                             workers=4)
    # Getting vectors for words
    word_vectors_Amenity = model_Amenity.wv
    # Getting the average vector for each document
    df['clean_description_col_vector'] = df['clean_description_col_processed'].apply(
        lambda x: sum([word_vectors_Amenity[word] for word in x if word in word_vectors_Amenity] or [0]) / len(x))

    # Splitting each line into two tokens: numbers and letters


    df['clean_string_col_processed'] = df[clean_string_col].apply(tokenize)
    tokens = df['clean_string_col_processed'].tolist()
    # Creating a Word2Vec Model
    model = Word2Vec(sentences=tokens, vector_size=2, window=5, min_count=1, workers=4)
    # Getting vectors for words
    word_vectors = model.wv
    # we get vectors for all tokens and combine them
    df['clean_string_col_vector'] = df['clean_string_col_processed'].apply(
        lambda x: sum([word_vectors[word] for word in x if word in word_vectors] or [0]) / len(x))

    # Text preprocessing
    df['clean_rn_col_processed'] = df[clean_rn_col].apply(lambda x: simple_preprocess(x))
    # Learning the Word2Vec model
    model = Word2Vec(sentences=df['clean_rn_col_processed'], vector_size=3, window=5, min_count=1, workers=4)
    # Getting vectors for words
    word_vectors = model.wv
    # Getting the average vector for each document
    df['clean_rn_col_vector'] = df['clean_rn_col_processed'].apply(
        lambda x: sum([word_vectors[word] for word in x if word in word_vectors] or [0]) / len(x))

    df.drop([clean_string_col, clean_description_col, 'clean_description_col_processed', 'clean_string_col_processed',
             clean_rn_col, 'clean_rn_col_processed'], axis=1, inplace=True)

    # for_scaling = ['Beds', 'Baths', 'sq.ft', 'Floor', 'Days_Till_Available', 'Units', 'Estiamted_Vacancy', 'Move_in_date_day', 'Move_in_date_month', 'Move_in_date_year']
    for_scaling = cfg.for_scaling
    scaler = StandardScaler()
    for scale in for_scaling:
        df[[scale]] = scaler.fit_transform(df[[scale]])

    # Processing vectors columns into separate single value columns to build a model further.
    # columns_to_split = ['clean_string_col_vector','clean_description_col_vector', 'clean_rn_col_vector']
    split_dfs = [split_vectors(df, column) for column in cfg.columns_to_split]
    df_split = pd.concat(split_dfs, axis=1)

    split_dfs = pd.DataFrame(df_split)
    df = pd.concat([df, split_dfs], axis=1)



    df.drop(cfg.columns_to_split, axis=1, inplace=True)



    X = df.drop(cfg.target_col, axis=1)
    y = df[[cfg.target_col]]

    return X, y


# all validations should be in the notebooks and should be executes only once, not every time, do not forget to save everything
def validate_features(X, y):
    """
    Validate features for ZenML pipeline

    """

    #execute it only once, not every time.
    #for x and y

    context = gx.get_context(project_root_dir = "services")
    ds_x = context.sources.add_or_update_pandas(name = "data_transform")
    da_x = ds_x.add_dataframe_asset(name = "pandas_dataframe")
    batch_request_x = da_x.build_batch_request(dataframe = X)

    ds_y = context.sources.add_or_update_pandas(name = "target_transform")
    da_y = ds_y.add_dataframe_asset(name = "pandas_dataframe")
    batch_request_y = da_y.build_batch_request(dataframe = y)

    # Create checkpoint
    checkpoint = context.add_or_update_checkpoint(
        name="my_checkpoint",
        validations=[
        {
            "batch_request": batch_request_x,
            "expectation_suite_name": "data_transform_expectation",
        },
        {
            "batch_request": batch_request_y,
            "expectation_suite_name": "target_transform_expectation",
        },
    ],
    )

    result = checkpoint.run()


    if result.success:
        return X, y


def load_features(X, y, version):
    cfg = compose(config_name="ApartmentPrice")
    # concatinate and save like a one dataframe
    df = pd.concat([X, y], axis=1)
    zenml.save_artifact(data=df, name="features_target", tags=[version])

    client = Client()

    l = client.list_artifacts(name="features_target", sort_by="version").items
    l.reverse()
    df = l[0].load()

    saved_X = df.drop(cfg.target_col, axis=1)
    saved_y = df[[cfg.target_col]]

    return saved_X, saved_y


if __name__ == "__main__":
    sample_data()
