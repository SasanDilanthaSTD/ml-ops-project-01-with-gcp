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
from pathlib import Path

# __file__ points to 'config/path_config.py'
# .resolve() makes it an absolute path
# .parent is the 'config' folder
# .parent.parent is the 'ml-ops-project_1' folder (your project root)
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "models"

RAW_DIR = BASE_DIR / Path("artifacts/raw")
RAW_DATA_PATH = RAW_DIR / Path("raw_data.csv")
TRAIN_DATA_PATH = RAW_DIR / Path("train_data.csv")
TEST_DATA_PATH = RAW_DIR / Path("test_data.csv")
CONFIG_PATH = BASE_DIR / Path("config/config.yml")

######################################## DATA PROCESSING PATHS ########################################
DATA_PROCESSING_DIR = BASE_DIR / Path("artifacts/data_processing")
PROCESSED_TRAIN_DATA_PATH = DATA_PROCESSING_DIR / Path("processed_train_data.csv")
PROCESSED_TEST_DATA_PATH = DATA_PROCESSING_DIR / Path("processed_test_data.csv")
