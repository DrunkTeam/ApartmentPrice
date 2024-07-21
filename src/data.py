import os
import dvc.api
import pandas as pd
import zenml
import numpy as np
import great_expectations as gx
import dvc.api
import datetime as dt
import re

from omegaconf import DictConfig
from hydra.core.global_hydra import GlobalHydra
from hydra import compose, initialize
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from gensim.models import Word2Vec
from gensim.utils import simple_preprocess
from pathlib import Path



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


# @hydra.main(config_path="../configs", config_name = "main", version_base=None)
def sample_data(cfg=cfg):
    # import os
    # os.chdir("/home/kama/ApartmentPrice")
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
    initialize(config_path="../configs", version_base="1.1")
    cfg = compose(config_name="data_version")
    version_num = cfg.data_version

    sample_path = Path("data") / "samples" / "sample.csv"
    df = pd.read_csv(sample_path)
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

    # cols_most_frequent = ['Days_Till_Available', 'Northern_Exposure', 'Southern_Exposure', 'Eastern_Exposure', 'Western_Exposure', 'Balcony', 'Walk_In_Closet', 'Fireplace',
    #                       'City_Skyline', 'Kitchen_Island', 'Stainless_Appliances', 'Renovated', 'Office_Space', 'building_id', 'Unique_ID']

    cols_most_frequent = cfg.columns_most_frequent
    for i in cols_most_frequent:
        df[[i]] = imp_most_frequent.fit_transform(df[[i]])

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

    # # validate_after_preprocessing(X,y)
    # #execute it only once, not every time.
    # #for x

    # context = gx.get_context(project_root_dir = "services")
    # ds_x = context.sources.add_or_update_pandas(name = "transformed_data")
    # da_x = ds_x.add_dataframe_asset(name = "pandas_dataframe")
    # batch_request_x = da_x.build_batch_request(dataframe = X)

    # # Create validator for X
    # # validator_x = context.get_validator(
    # #     batch_request=batch_request_x,
    # #     expectation_suite_name='transformed_data_expectation',
    # # )

    # ds_y = context.sources.add_or_update_pandas(name = "transformed_target")
    # da_y = ds_y.add_dataframe_asset(name = "pandas_dataframe")
    # batch_request_y = da_y.build_batch_request(dataframe = y)

    # # validator_y = context.get_validator(
    # #     batch_request=batch_request_y,
    # #     expectation_suite_name='transformed_target_expectation',
    # # )

    # # Create checkpoint
    # checkpoint = context.add_or_update_checkpoint(
    #     name="my_checkpoint",
    #     validations=[
    #     {
    #         "batch_request": batch_request_x,
    #         "expectation_suite_name": "transformed_data_expectation",
    #     },
    #     {
    #         "batch_request": batch_request_y,
    #         "expectation_suite_name": "transformed_target_expectation",
    #     },
    # ],
    # )

    # # checkpoint_x = context.add_or_update_checkpoint(
    # #     name="checkpoint_x",
    # #     validator=validator_x,
    # # )

    # # retrieved_checkpoint_x = context.get_checkpoint(name="checkpoint_x")

    # result = checkpoint.run()

    # assert checkpoint_result_x.success

    # for y

    # retrieved_checkpoint_y = context.get_checkpoint(name="checkpoint_y")

    # checkpoint_result_y = retrieved_checkpoint_y.run()

    # assert checkpoint_result_y.success

    # initialize(config_path="../configs/data", version_base="1.1")
    cfg = compose(config_name="ApartmentPrice")

    context = gx.get_context()
    ds_x = context.sources.add_or_update_pandas(name="transformed_data")
    da_x = ds_x.add_dataframe_asset(name="pandas_dataframe")
    batch_request_x = da_x.build_batch_request(dataframe=X)

    # Create expectations suite
    context.add_or_update_expectation_suite('transformed_data_expectation')

    # Create validator for X
    validator_x = context.get_validator(
        batch_request=batch_request_x,
        expectation_suite_name='transformed_data_expectation',
    )

    # Assume all ohe-transformed cols are 0 or 1
    for col in list(cfg.ohe_cols):
        validator_x.expect_column_values_to_be_in_set(
            column=col,
            value_set=[0, 1]
        )

    # all columns are not null
    for col in list(cfg.validation_columns):
        validator_x.expect_column_values_to_not_be_null(
            column=col
        )

        # some columns should be float

    for col in cfg.validation_columns:
        validator_x.expect_column_values_to_be_of_type(
            column=col,
            type_="float"
        )

    # some columns should be int
    for col in cfg.int_columns:
        validator_x.expect_column_values_to_be_of_type(
            column=col,
            type_="int"
        )

        # Store expectation suite
    validator_x.save_expectation_suite(
        discard_failed_expectations=False
    )

    # Create checkpoint
    checkpoint_x = context.add_or_update_checkpoint(
        name="checkpoint_x",
        validator=validator_x,
    )

    # Run validation
    checkpoint_result_x = checkpoint_x.run()

    ds_y = context.sources.add_or_update_pandas(name="transformed_target")
    da_x = ds_y.add_dataframe_asset(name="pandas_dataframe")
    batch_request_y = da_x.build_batch_request(dataframe=y)
    # Create expectations suite
    context.add_or_update_expectation_suite('transformed_target_expectation')

    validator_y = context.get_validator(
        batch_request=batch_request_y,
        expectation_suite_name='transformed_target_expectation',
    )
    # Assume Price between 0 and 12091
    validator_y.expect_column_values_to_be_between(
        column='Price',
        min_value=0,
        max_value=12091,
    )

    # Store expectation suite
    validator_y.save_expectation_suite(
        discard_failed_expectations=False
    )

    # Create checkpoint
    checkpoint_y = context.add_or_update_checkpoint(
        name="checkpoint_y",
        validator=validator_y,
    )

    # Run validation
    checkpoint_result_y = checkpoint_y.run()

    if checkpoint_result_x.success and checkpoint_result_y.success:
        return X, y

    # if result.success:
    #     return X, y


def load_features(X, y, version):
    # concatinate and save like a one dataframe
    df = df = pd.concat([X, y], axis=1)
    zenml.save_artifact(data=df, name="features_target", tags=[version])
    # zenml.save_artifact(data = y, name = "target", tags = [version])


if __name__ == "__main__":
    sample_data()
