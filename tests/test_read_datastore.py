# import unittest
# from unittest.mock import patch
# from pathlib import Path

# import pandas as pd

# from src.data import read_datastore


# class TestReadDatastore(unittest.TestCase):
#     @patch("src.data.initialize")
#     @patch("src.data.compose")
#     @patch("src.data.pd.read_csv")
#     def test_read_datastore(self, mock_read_csv, mock_compose, mock_initialize):
#         # Set up the mock config and return values
#         mock_compose.return_value.sample_num = "v1.0"
#         mock_df = pd.DataFrame({"column1": [1, 2, 3], "column2": [4, 5, 6]})
#         mock_read_csv.return_value = mock_df

#         # Call the method
#         df, version_num = read_datastore()

#         # Assertions
#         self.assertEqual(version_num, "v1.0")
#         pd.testing.assert_frame_equal(df, mock_df)
#         mock_initialize.assert_called_with(config_path="../configs", version_base="1.1")
#         mock_compose.assert_called_with(config_name="sample_data")
#         mock_read_csv.assert_called_with(Path("data") / "samples" / "sample.csv")


# if __name__ == "__main__":
#     unittest.main()        
# import unittest
# from unittest.mock import patch
# from pathlib import Path
# import pandas as pd
# from src.data import read_datastore

# class TestReadDatastore(unittest.TestCase):
#     @patch("src.data.initialize")
#     @patch("src.data.compose")
#     @patch("src.data.pd.read_csv")
#     def test_read_datastore(self, mock_read_csv, mock_compose, mock_initialize):
#         # Set up the mock config and return values
#         mock_compose.return_value.sample_num = "1.0"
#         mock_df = pd.DataFrame({"column1": [1, 2, 3], "column2": [4, 5, 6]})
#         mock_read_csv.return_value = mock_df

#         # Call the method
#         df, version_num = read_datastore()

#         # Assertions
#         self.assertEqual(version_num, "v1.0")
#         pd.testing.assert_frame_equal(df, mock_df)
#         mock_initialize.assert_called_with(config_path="../configs", version_base="1.1")
        
#         mock_compose.assert_called_with(config_name="sample_data")
#         mock_read_csv.assert_called_with(Path("data") / "samples" / "sample.csv")

# if __name__ == "__main__":
#     unittest.main()
import unittest
from unittest.mock import patch, Mock
import pandas as pd
from io import StringIO

# Импорт функции из вашего модуля
from src.data import read_datastore

class TestReadDatastore(unittest.TestCase):

    @patch('src.data.dvc.api.get_url')
    @patch('src.data.pd.read_csv')
    @patch('src.data.cfg')
    def test_read_datastore(self, mock_cfg, mock_read_csv, mock_get_url):
        # Mock configuration settings
        mock_cfg.data.path = 'data/raw/Equity_Apartments_Data.csv'
        mock_cfg.data.remote = 'localstore'
        mock_cfg.data.repo = '.'
        mock_cfg.data.version = 'v1.0'
        
        # Create a sample dataframe
        # mocked_url = "col1,col2\nval1,val2"
        # sample_df = pd.read_csv(StringIO(mocked_url))

        mock_df = pd.DataFrame({"column1": [1, 2, 3], "column2": [4, 5, 6]})
        mock_read_csv.return_value = mock_df
        
        # # Mock the URL returned by dvc.api.get_url
        # mock_get_url.return_value = mocked_url
        
        
        # Call the function to test
        df, version_num = read_datastore()
        
        # Assertions to verify the behavior
        # mock_get_url.assert_called_once_with(
        #     path='data/raw/Equity_Apartments_Data.csv',
        #     remote='localstore',
        #     repo='.',
        #     rev='v1.0'
        # )
        # mock_read_csv.assert_called_once_with('mocked_url')
        
        self.assertEqual(version_num, 'v1.0')
        pd.testing.assert_frame_equal(df, mock_df)

if __name__ == '__main__':
    unittest.main()

