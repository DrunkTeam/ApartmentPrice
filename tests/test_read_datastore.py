import unittest
from unittest.mock import patch
import pandas as pd

from src.data import read_datastore
from src.data import init_hydra


class TestReadDatastore(unittest.TestCase):
    @patch("src.data.dvc.api.get_url")
    @patch("src.data.pd.read_csv")
    def test_read_datastore(self, mock_read_csv, mock_get_url):
        # Set up the mock config and return values
        mock_get_url.return_value = "mock_data_url"
        mock_df = pd.DataFrame({"column1": [1, 2, 3], "column2": [4, 5, 6]})
        mock_read_csv.return_value = mock_df
        cfg = init_hydra()
        mock_cfg = cfg

        with patch("src.data.cfg", mock_cfg):
            # Call the method
            df, version_num = read_datastore()

        # Assertions
        self.assertEqual(version_num, "v1.0")
        pd.testing.assert_frame_equal(df, mock_df)
        mock_get_url.assert_called_with(
            path=cfg.data.path,
            remote=cfg.data.remote,
            repo=cfg.data.repo,
            rev=str(cfg.data.version)
        )
        mock_read_csv.assert_called_with("mock_data_url")


if __name__ == "__main__":
    unittest.main()
