import os
from pathlib import Path
import pandas as pd
from google.cloud import storage
from sklearn.model_selection import train_test_split
from src.logger import get_logger
from src.custom_exception import CustomException
from config.path_config import *
from utils.common_functions import read_yml_file

# Initialize logger
logger_obj = get_logger(__name__)

# create DataIngetion claa
class DataIngestion:
    def __init__(self, config):
        self.__config = config["data_ingestion"]
        self.__gcp_bucket_name = self.__config["bucket_name"]
        self.__file_nme = self.__config["bucket_file_name"]
        self.__train_test_split_ratio =  self.__config["train_ratio"]

        # create RAW data derectory if not exists
        os.makedirs(Path(RAW_DIR), exist_ok=True)
        
        logger_obj.info(f"================> Data ingestion started with GCP bucket: {self.__gcp_bucket_name} and file: {self.__file_nme}")
        
    # doenloade data from GCP bucket
    def __download_data_from_gcp(self):
        """_summary_
        This function downloads the data file from the specified GCP bucket
        and saves it to the RAW_DATA_PATH.

        Raises:
            CustomException: If there is an error during the download process.
        """
        try:
            client = storage.Client()
            bucket = client.bucket(self.__gcp_bucket_name)
            blob = bucket.blob(self.__file_nme)

            # Download the file to RAW_DATA_PATH
            blob.download_to_filename(Path(RAW_DATA_PATH))
            
            logger_obj.info(f"---:) Data downloaded successfully from GCP bucket {self.__gcp_bucket_name} to {RAW_DATA_PATH}")
        except Exception as ex:
            logger_obj.error(f"---:( Error downloading data from GCP: {ex}")
            raise CustomException(f"---:( Data download failed: {ex}")
        
    # split data into train and test sets
    def __split_data(self):
        """_summary_
        This function splits the raw data into training and testing datasets
        based on the specified train-test split ratio.

        Raises:
            CustomException: If there is an error during the data splitting process.
        """
        try:
            # read the data set
            data = pd.read_csv(RAW_DATA_PATH)
            
            # split the data
            train_data, test_data = train_test_split(
                data,
                test_size=1-self.__train_test_split_ratio,
                random_state=42
            )
            
            # save the train and test data
            train_data.to_csv(Path(TRAIN_DATA_PATH), index=False)
            logger_obj.info(f"---:) Training data saved at {TRAIN_DATA_PATH}")
            
            test_data.to_csv(Path(TEST_DATA_PATH), index=False)
            logger_obj.info(f"---:) Testing data saved at {TEST_DATA_PATH}")
        except Exception as ex:
            logger_obj.error(f"---:( Error splitting data: {ex}")
            raise CustomException(f"---:( Data splitting failed: {ex}")
        
    # run data ingestion process
    def run(self):
        """_summary_
        This function orchestrates the data ingestion process by downloading
        the data from GCP and splitting it into training and testing datasets.
        """
        try:
            # download data from GCP storage
            self.__download_data_from_gcp()
            
            # split the data into train and test sets
            self.__split_data()
            
            logger_obj.info("---:) Data ingestion process completed successfully.")
        except Exception as ex:
            logger_obj.error(f"---:( Data ingestion process failed: {ex}")
            raise CustomException(f"---:( Data ingestion failed: {ex}")
        finally:
            logger_obj.info("================> Data ingestion process finished.")
            

if __name__ == "__main__":
    # create config yml obj 
    config = read_yml_file(Path(CONFIG_PATH))
    
    # create DataIngestion obj
    data_ingestion = DataIngestion(config=config)

    # run the data ingestion process
    data_ingestion.run()