import unittest
from unittest.mock import patch, MagicMock, mock_open
import pandas as np
import pandas as pd
from datetime import datetime

# Предполагается, что функции и модули src.data импортированы здесь
from src.data import preprocess_data

# Пример данных для тестирования
DATA = {
    'Unnamed: 0': [0, 1, 2],
    'unit_id': ['U1', 'U2', 'U3'],
    'Apartment Name': ['Apt1', 'Apt2', 'Apt3'],
    'URL': ['url1', 'url2', 'url3'],
    'building_id': ['B1', 'B2', 'B3'],
    'clean_rn_col': ['This is A TEST', 'Another TEST row', 'The last one'],
    'clean_description_col': ['Description 1', 'Description 2', 'Description 3'],
    'feature1': ['a', 'b', 'c'],
    'City': ['Boston', 'Denver', 'New York City'],
    'Day_of_the_week_recorded': ['Tuesday', 'Friday', 'Monday'],
    'Day_Recorded': [datetime(2022, 1, 1), datetime(2022, 1, 2), datetime(2022, 1, 3)],
    'Days_Till_Available': [10.0, 20.0, 30.0],
    'Move_in_date': [datetime(2022, 1, 11), datetime(2022, 1, 22), datetime(2022, 2, 2)], # New column
    'target': [100, 200, 300],
}


class TestPreprocessData(unittest.TestCase):
    @patch('src.data.compose')
    @patch('src.data.pd.get_dummies')
    @patch('src.data.Word2Vec')
    @patch('builtins.open', new_callable=mock_open)
    def test_preprocess_data(self, mock_open, mock_word2vec, mock_get_dummies, mock_compose):
        # Настройка мока для конфигурации
        mock_cfg = MagicMock()
        mock_cfg.dublicate_cols = ['unit_id', 'Apartment Name', 'URL', 'building_id']
        mock_cfg.clean_rn_columns = 'clean_rn_col'
        mock_cfg.clean_description_columns = 'clean_description_col'
        mock_cfg.clean_string_columns = 'feature1'
        mock_cfg.columns_most_frequent = ['feature1']
        mock_cfg.todatatime_columns = 'Day_Recorded'
        mock_cfg.col_for_imputing_date = 'Days_Till_Available'
        mock_cfg.col_for_new_date = 'new_date'
        mock_cfg.col_for_old_date = 'Move_in_date'
        mock_cfg.ohe_columns = 'City'
        mock_cfg.columns_for_label_enc = 'Day_of_the_week_recorded'
        mock_cfg.label_encoding = {'Tuesday': 1, 'Saturday': 2, 'Friday': 3, 'Sunday': 4, 'Monday': 5, 'Wednesday': 6, 'Thursday': 7}
        mock_cfg.for_scaling = ['Days_Till_Available']
        mock_cfg.columns_to_split = ['clean_string_col_vector', 'clean_description_col_vector', 'clean_rn_col_vector']
        mock_cfg.target_col = 'target'
        mock_compose.return_value = mock_cfg

        # Настройка мока для get_dummies
        mock_get_dummies.return_value = pd.DataFrame({
            'Boston': [1, 0, 0],
            'Denver': [0, 1, 0],
            'New York City': [0, 0, 1],
        })

        # Настройка мока для Word2Vec
        mock_w2v_model = MagicMock()
        mock_w2v_model.wv = MagicMock()
        mock_w2v_model.wv.__contains__.side_effect = lambda x: True
        mock_w2v_model.wv.__getitem__.side_effect = lambda x: np.array([1, 1, 1])
        mock_word2vec.return_value = mock_w2v_model

        # Создание DataFrame
        df = pd.DataFrame(DATA)

        # Вызов тестируемой функции
        X, y = preprocess_data(df)

        # Проверка результатов
        self.assertNotIn('Unnamed: 0', X.columns)
        self.assertNotIn('unit_id', X.columns)
        self.assertNotIn('Apartment Name', X.columns)
        self.assertNotIn('URL', X.columns)
        self.assertNotIn('building_id', X.columns)
        self.assertIn('Boston', X.columns)
        self.assertIn('Denver', X.columns)
        self.assertIn('New York City', X.columns)
        self.assertIn('Days_Till_Available', X.columns)
        self.assertEqual(y.shape[1], 1)
        self.assertEqual(y.columns[0], 'target')

        # Проверка вызова get_dummies
        mock_get_dummies.assert_called_once()
        pd.testing.assert_series_equal(
            mock_get_dummies.call_args[0][0],
            df['City']
        )

        # Проверка вызова Word2Vec
        mock_word2vec.assert_called()


if __name__ == '__main__':
    unittest.main()
