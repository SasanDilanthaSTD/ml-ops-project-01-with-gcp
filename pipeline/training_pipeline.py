from src.data_ingestion import DataIngestion
from src.data_preprocessing import DataProcessor
from src.model_training import ModelTrainer
from utils.common_functions import read_yml_file
from config.path_config import *


if __name__ == "__main__":
    # Step 1: Data Ingestion
    config = read_yml_file(Path(CONFIG_PATH))
    data_ingestion = DataIngestion(config=config)
    data_ingestion.run()
    
    # Step 2: Data Preprocessing
    data_processor = DataProcessor(
        config_path=CONFIG_PATH,
        train_path=TRAIN_DATA_PATH,
        test_path=TEST_DATA_PATH,
        processed_dir=DATA_PROCESSING_DIR
    )
    data_processor.process()
    
    # Step 3: Model Training
    trainer = ModelTrainer(
        train_data_path=PROCESSED_TRAIN_DATA_PATH,
        test_data_path=PROCESSED_TEST_DATA_PATH,
        model_output_path=MODEL_OUTPUT_PATH
    )
    trainer.run()
