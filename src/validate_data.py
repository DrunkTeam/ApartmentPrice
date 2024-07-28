import great_expectations as gx
from great_expectations.data_context import FileDataContext


def validate_initial_data(csv_path, name_suit="my_expectation_suite"):
    context = FileDataContext(project_root_dir="../services")
    ds = context.sources.add_or_update_pandas(name="my_pandas_ds")
    da = ds.add_csv_asset(
        name="csv_asset",
        filepath_or_buffer=csv_path,
    )
    batch_request = da.build_batch_request()
    batches = da.get_batch_list_from_batch_request(batch_request)
    context.add_or_update_expectation_suite(name_suit)
    validator = context.get_validator(
        batch_request=batch_request,
        expectation_suite_name=name_suit
    )

    validator.expect_column_values_to_be_between(column="Price", min_value=0)
    validator.expect_column_values_to_not_be_null(column="Price")
    validator.expect_column_values_to_be_of_type(column="Price", type_="int")
    validator.expect_column_values_to_be_between(column="Beds", min_value=0, max_value=10)
    validator.expect_column_values_to_not_be_null(column="Beds")
    validator.expect_column_values_to_match_regex(column="Beds", regex="^\d+$")
    validator.expect_column_values_to_be_between(column="Baths", min_value=0, max_value=10)
    validator.expect_column_values_to_not_be_null(column="Baths")
    validator.expect_column_values_to_match_regex(column="Baths", regex="^\d+$")
    validator.expect_column_values_to_be_between(column="sq.ft", min_value=0)
    validator.expect_column_values_to_not_be_null(column="sq.ft")
    validator.expect_column_values_to_match_regex(column="sq.ft", regex="^\d+(\.\d{1})?$")
    validator.expect_column_values_to_be_between(column="Floor", min_value=0, max_value=100)
    validator.expect_column_values_to_not_be_null(column="Floor")
    validator.expect_column_values_to_match_regex(column="Floor", regex="^\d+$")
    validator.expect_column_values_to_match_strftime_format(column="Move_in_date", strftime_format="%Y-%m-%d")
    validator.expect_column_values_to_not_be_null(column="Move_in_date")
    validator.expect_column_values_to_be_between(
        column="Move_in_date",
        min_value="2021-06-25",
        max_value="2021-07-17"
    )
    validator.expect_column_values_to_match_regex(column="unit_id", regex="^[a-zA-Z0-9]+$")
    validator.expect_column_values_to_not_be_null(column="unit_id")
    validator.expect_column_values_to_be_unique(column="unit_id")
    validator.save_expectation_suite(discard_failed_expectations=False)

    result = context.run_checkpoint(name="my_checkpoint", validations=[
        {
            "batch_request": batch_request,
            "expectation_suite_name": name_suit,
        },
    ])

    return result.success
