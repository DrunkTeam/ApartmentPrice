import pandas as pd
import pytest

@pytest.fixture()
def some_data():
	"""
	Loads some data 
	"""
	df = pd.read_csv("data/raw/Equity_Apartments_Data.csv")
	return df

# some_data is the function name (fixture)
def test_some_data(some_data):
    assert len(some_data) > 0