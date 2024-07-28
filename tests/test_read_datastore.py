import unittest
import pandas as pd
from unittest.mock import patch, MagicMock
from src.data import read_datastore


class TestReadDatastore(unittest.TestCase):
    @patch("src.data.dvc.api.get_url")
    @patch("src.data.pd.read_csv")
    @patch("src.data.init_hydra")
    def test_read_datastore(self, mock_init_hydra, mock_read_csv, mock_get_url):
        # Set up the mock config and return values
        mock_get_url.return_value = "mock_data_url"
        mock_df = pd.DataFrame({"column1": [1, 2, 3], "column2": [4, 5, 6]})
        mock_read_csv.return_value = mock_df

        # Mock configuration
        mock_cfg = MagicMock()
        mock_cfg.data.path = "data/raw/Equity_Apartments_Data.csv"
        mock_cfg.data.remote = "localstore"
        mock_cfg.data.repo = "."
        mock_cfg.data.version = "v1.0"
        mock_init_hydra.return_value = mock_cfg

        with patch("src.data.cfg", mock_cfg):
            # Call the method
            df, version_num = read_datastore()

        # Assertions
        self.assertEqual(version_num, "v1.0")
        pd.testing.assert_frame_equal(df, mock_df)
        mock_get_url.assert_called_with(
            path=mock_cfg.data.path,
            remote=mock_cfg.data.remote,
            repo=mock_cfg.data.repo,
            rev=str(mock_cfg.data.version)
        )
        mock_read_csv.assert_called_with("mock_data_url")


if __name__ == "__main__":
    unittest.main()
