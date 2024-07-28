import unittest
from unittest.mock import patch, MagicMock

from src.validate_data import validate_initial_data


class TestValidateInitialData(unittest.TestCase):
    @patch("src.validate_data.FileDataContext")
    def test_validate_initial_data(self, MockFileDataContext):
        # Mock the context and other components
        mock_context = MockFileDataContext.return_value
        mock_source = mock_context.sources.add_or_update_pandas.return_value
        mock_asset = mock_source.add_csv_asset.return_value
        mock_batch_request = mock_asset.build_batch_request.return_value
        mock_checkpoint = mock_context.run_checkpoint.return_value
        mock_checkpoint.success = True

        csv_path = "mock_data.csv"

        # Call the method
        result = validate_initial_data(csv_path)

        # Assertions
        self.assertTrue(result)
        mock_context.sources.add_or_update_pandas.assert_called_with(name="my_pandas_ds")
        mock_source.add_csv_asset.assert_called_with(name="csv_asset", filepath_or_buffer=csv_path)
        mock_context.get_validator.assert_called_with(
            batch_request=mock_batch_request, expectation_suite_name="my_expectation_suite"
        )
        mock_context.run_checkpoint.assert_called()


if __name__ == "__main__":
    unittest.main()
