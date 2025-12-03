import os
import pandas as pd
from src.logger import get_logger
from src.custom_exception import CustomException
import yaml

logger_obj = get_logger(__name__) 

# read yaml file
def read_yml_file(file_path: str) -> dict:
    """_summary_
    This function reads a YAML file and returns its contents as a dictionary.

    Args:
        file_path (str): The path to the YAML file.
    Returns:
        dict: The contents of the YAML file as a dictionary.
    """
    try:
        if not os.path.exists(file_path):
            logger_obj.error(f"YAML file not found at path: {file_path}")
            raise CustomException(f"YAML file not found at path: {file_path}")
        
        with open(file=file_path, mode="r") as yml_file:
            yml_file_content = yaml.safe_load(yml_file)
            logger_obj.info(f"Successfully readed yml file at {file_path}")
            return yml_file_content
    except Exception as e:
        logger_obj.error(f"Error reading YAML file at {file_path}: {e}")
        raise CustomException(f"YML file loading failed: {e}")