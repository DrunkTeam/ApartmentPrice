from src.data import read_datastore, preprocess_data
from hydra import compose, initialize
import great_expectations as gx


def validate_after_preprocessing(X, y):
    # initialize(config_path="../configs", version_base="1.1")
    cfg = compose(config_name="ApartmentPrice")

    context = gx.get_context(project_root_dir="services")

    ds_x = context.sources.add_or_update_pandas(name="data_transform")
    da_x = ds_x.add_dataframe_asset(name="pandas_dataframe")
    batch_request_x = da_x.build_batch_request(dataframe=X)

    # Create expectations suite
    context.add_or_update_expectation_suite('data_transform_expectation')

    # Create validator for X
    validator_x = context.get_validator(
        batch_request=batch_request_x,
        expectation_suite_name='data_transform_expectation'
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
        # попробовать добавить expectation about NUMERIC
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

    ds_y = context.sources.add_or_update_pandas(name="target_transform")
    da_x = ds_y.add_dataframe_asset(name="pandas_dataframe")
    batch_request_y = da_x.build_batch_request(dataframe=y)
    # Create expectations suite
    context.add_or_update_expectation_suite('target_transform_expectation')

    validator_y = context.get_validator(
        batch_request=batch_request_y,
        expectation_suite_name='target_transform_expectation',
    )
    # Assume Price between 0 and 12091
    validator_y.expect_column_values_to_be_between(
        column='Price',
        min_value=0,
        max_value=12091
    )

    # Store expectation suite
    validator_y.save_expectation_suite(
        discard_failed_expectations=False
    )

    # Create checkpoint
    checkpoint = context.add_or_update_checkpoint(
        name="checkpoint",
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

    # Run validation
    checkpoint_result = checkpoint.run()

    if checkpoint_result.success:
        return X, y


if __name__ == "__main__":
    df, _ = read_datastore()
    X, y = preprocess_data(df)
    X, y = validate_after_preprocessing(X, y)
