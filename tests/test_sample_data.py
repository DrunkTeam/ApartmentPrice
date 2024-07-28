import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import os

from src.data import sample_data

# Example of configuration you use in the function
mock_cfg = MagicMock()
mock_cfg.data.path = 'data/samples/sample.csv'
mock_cfg.data.remote = "localstore"
mock_cfg.data.repo = "."
mock_cfg.data.version = "v1.0"
mock_cfg.data.sample_size = 0.1
mock_cfg.data.random_state = 42


class TestSampleData(unittest.TestCase):

    @patch('src.data.compose')
    @patch('src.data.download_dataset')
    @patch('src.data.dvc.api.get_url')
    @patch('src.data.pd.read_csv')
    @patch('src.data.os.system')
    def test_sample_data(self, mock_system, mock_read_csv, mock_get_url, mock_download_dataset, mock_compose):
        # Setting up a mock for compose
        mock_compose.return_value = mock_cfg

        # Setting up a mock for dvc.api.get_url
        mock_get_url.return_value = 'mock_data_url'

        # Create fake data for pandas.read_csv
        fake_data = pd.DataFrame({'col1': range(100)})
        mock_read_csv.return_value = fake_data

        # Call the function under test
        sample_data(mock_cfg)

        # Call Check
        mock_download_dataset.assert_called_once()
        mock_get_url.assert_called_once_with(
            path=mock_cfg.data.path,
            remote=mock_cfg.data.remote,
            repo=mock_cfg.data.repo,
            rev=mock_cfg.data.version
        )
        mock_read_csv.assert_called_once_with('mock_data_url')

        # Checking the correctness of data sampling
        expected_sample = fake_data.sample(frac=mock_cfg.data.sample_size, random_state=mock_cfg.data.random_state)
        pd.testing.assert_frame_equal(
            mock_read_csv.return_value.sample(frac=mock_cfg.data.sample_size, random_state=mock_cfg.data.random_state),
            expected_sample)

        # Check that the directory and file were created
        self.assertTrue(os.path.exists('data/samples/sample.csv'))

        # Checking os.system calls
        mock_system.assert_any_call('dvc add data/samples/sample.csv')
        mock_system.assert_any_call('dvc push')


if __name__ == '__main__':
    unittest.main()
