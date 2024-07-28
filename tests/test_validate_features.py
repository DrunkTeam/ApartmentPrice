import unittest
from unittest.mock import patch

import pandas as pd

from src.data import validate_features

X = pd.DataFrame(
    {
        "Beds": [-0.420357253205981],
        "Baths": [-0.7457859518255723],
        "sq.ft": [-0.3477852098030933],
        "Floor": [-0.5967570384857163],
        "Units": [1.376596993666781],
        "Northern_Exposure": [0.0],
        "Southern_Exposure": [0.0],
        "Eastern_Exposure": [0.0],
        "Western_Exposure": [0.0],
        "Balcony": [1.0],
        "Walk_In_Closet": [1.0],
        "Fireplace": [0.0],
        "City_Skyline": [0.0],
        "Kitchen_Island": [0.0],
        "Stainless_Appliances": [0.0],
        "Renovated": [0.0],
        "Office_Space": [0.0],
        "Days_Till_Available": [-1.0113690088528615],
        "Day_of_the_week_recorded": [6.0],
        "Estiamted_Vacancy": [-0.4452019625631747],
        "Move_in_date_day": [-1.1629431091955773],
        "Move_in_date_month": [-0.7073211509072912],
        "Boston": [0.0],
        "Denver": [0.0],
        "Los Angeles": [1.0],
        "New York City": [0.0],
        "Orange County": [0.0],
        "San Diego": [0.0],
        "San Francisco": [0.0],
        "Seattle": [0.0],
        "Washington DC": [0.0],
        "clean_string_col_vector_0": [0.13289379],
        "clean_string_col_vector_1": [0.09964815],
        "clean_description_col_vector_0": [0.29640728],
        "clean_description_col_vector_1": [-0.6220222],
        "clean_description_col_vector_2": [1.9212562],
        "clean_description_col_vector_3": [-0.6324686],
        "clean_description_col_vector_4": [-1.2204905],
        "clean_description_col_vector_5": [0.36333385],
        "clean_description_col_vector_6": [1.2960498],
        "clean_description_col_vector_7": [-0.4152936],
        "clean_description_col_vector_8": [-0.89173377],
        "clean_description_col_vector_9": [-0.8246506],
        "clean_rn_col_vector_0": [-0.76035964],
        "clean_rn_col_vector_1": [1.7885453],
        "clean_rn_col_vector_2": [-0.47801423]
    }
)
y = pd.DataFrame({"Price": [2774.0]})


class TestValidateFeatures(unittest.TestCase):
    @patch("src.data.gx.get_context")
    def test_validate_features(self, MockGetContext):
        # Mock the context and other components
        mock_context = MockGetContext.return_value
        mock_checkpoint_x = mock_context.add_or_update_checkpoint.return_value
        mock_checkpoint_result_x = mock_checkpoint_x.run.return_value
        mock_checkpoint_result_x.success = True

        mock_checkpoint_y = mock_context.add_or_update_checkpoint.return_value
        mock_checkpoint_result_y = mock_checkpoint_y.run.return_value
        mock_checkpoint_result_y.success = True

        # Call the method
        validated_X, validated_y = validate_features(X, y)

        # Assertions
        self.assertTrue((validated_X == X).all().all())
        self.assertTrue((validated_y == y).all().all())
        mock_context.sources.add_or_update_pandas.assert_called()
        mock_context.add_or_update_checkpoint.assert_called()
        mock_checkpoint_x.run.assert_called()
        mock_checkpoint_y.run.assert_called()


if __name__ == "__main__":
    unittest.main()
