"""_summary_
This module defines the file paths used in the project.
It constructs paths for data storage, model storage, and other resources
based on the current working directory.

Attributes:
    BASE_DIR (str): The base directory of the project.
    MODEL_DIR (str): The directory for storing model files.
    
    RAW_DATA_PATH (str): The path for raw data file.
    TRAIN_DATA_PATH (str): The path for training data file.
    TEST_DATA_PATH (str): The path for testing data file.
    
    CONFIG_PATH (str): The path for configuration file.
"""

import os

BASE_DIR = os.getcwd()
MODEL_DIR = os.path.join(BASE_DIR, "models")

RAW_DIR = os.path.join(BASE_DIR, "artifacts/raw")
RAW_DATA_PATH = os.path.join(RAW_DIR, "raw_data.csv")
TRAIN_DATA_PATH = os.path.join(RAW_DIR, "train_data.csv")
TEST_DATA_PATH = os.path.join(RAW_DIR, "test_data.csv")
CONFIG_PATH = os.path.join(BASE_DIR, "config", "config.yml")