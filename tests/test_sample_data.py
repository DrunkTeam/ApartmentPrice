import os
import pytest
import pandas as pd
from hydra import initialize, compose
from unittest.mock import patch
from src.data import sample_data
from src.validate_data import validate_initial_data

def mock_system(command):
    if command.startswith('dvc add') or command.startswith('dvc push'):
        return 0  # Mock success for DVC commands
    return os.system(command)

def test_sample_data_creates_file(tmp_path):
    # Change working directory to a temporary path
    os.chdir(tmp_path)
    
    # Ensure the required directory structure
    os.makedirs('data/samples', exist_ok=True)
    
    with initialize(config_path="../configs", job_name="test_app"):
        cfg = compose(config_name="test_config")
        
        with patch('os.system', side_effect=mock_system):
            sample_data(cfg)
        
        assert os.path.exists('data/samples/sample.csv'), "Sample file was not created."

def test_sample_data_not_empty(tmp_path):
    # Change working directory to a temporary path
    os.chdir(tmp_path)
    
    # Ensure the required directory structure
    os.makedirs('data/samples', exist_ok=True)
    
    with initialize(config_path="../configs", job_name="test_app"):
        cfg = compose(config_name="test_config")
        
        with patch('os.system', side_effect=mock_system):
            sample_data(cfg)
        
        sample_df = pd.read_csv('data/samples/sample.csv')
        
        assert not sample_df.empty, "Sample file is empty."

def test_validate_initial_data():
    csv_path = "../data/samples/sample.csv"
    validate_initial_data(csv_path)