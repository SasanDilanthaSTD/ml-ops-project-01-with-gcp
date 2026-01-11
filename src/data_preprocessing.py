import os
import pandas as pd
import numpy as np
from src.logger import get_logger
from src.custom_exception import CustomException
from config.path_config import *
from utils.common_functions import read_yml_file, load_data
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE

logger_obj = get_logger(__name__)

class DataProcessor:
    def __init__(self, config_path: str, train_path: str, test_path: str, processed_dir: str):
        self.config_load = read_yml_file(config_path)
        self.config = self.config_load.get("data_processing", {})
        self.train_path = train_path
        self.test_path = test_path
        self.processed_dir = processed_dir
        
        # if not exists, create processed data directory
        if not os.path.exists(self.processed_dir):
            os.makedirs(self.processed_dir)
            logger_obj.info(f"Created directory for processed data at {self.processed_dir}")
            
    def process_data(self, df: pd.DataFrame):
        try:
            logger_obj.info("[DataProcessor] : Starting data processing...")
            
            logger_obj.info("[DataProcessor] : Dropping the unused columns")
            df.drop(columns=['Booking_ID'], inplace=True)
            df.drop_duplicates(inplace=True)
            
            cat_cols = self.config.get("category_features", [])
            num_cols = self.config.get("numerical_features", [])
            
            logger_obj.info("[DataProcessor] : Applying Label Encoding to categorical columns")
            encoder = LabelEncoder()

            store_mappings = {}

            for col in cat_cols:
                df[col] = encoder.fit_transform(df[col])

                # mapping values
                store_mappings[col] = {lable:code for lable, code in zip(encoder.classes_, encoder.transform(encoder.classes_))}
            
            logger_obj.info("[DataProcessor] : Label Mapping are:")
            for col, mapping in store_mappings.items():
                logger_obj.info(f"{col} : {mapping}")
                
            logger_obj.info("[DataProcessor] : Skewness handling using log1p transformation")
            skewness_threshold = self.config.get("skewness_threshold", 5)
            skewness  = df[num_cols].apply(lambda x : x.skew())
            
            for col in skewness[skewness > skewness_threshold].index:
                df[col] = np.log1p(df[col])
                
            logger_obj.info("[DataProcessor] : Data processing completed.")
            return df
        except Exception as e:
            logger_obj.error(f"Error in data processing: {e}")
            raise CustomException(f"Data processing failed: {e}")
        
    def balance_data(self, df: pd.DataFrame):
        try:
            logger_obj.info("[DataProcessor] : Handling data imbalance using SMOTE")
            X = df.drop(columns=['booking_status'])
            y = df['booking_status']
            
            smote = SMOTE(random_state=42)
            X_resampled, Y_resampled = smote.fit_resample(X, y)
            
            balanced_data = pd.DataFrame(X_resampled, columns=X.columns)
            balanced_data['booking_status'] = Y_resampled
            logger_obj.info("[DataProcessor] : Data balancing completed.")
            return balanced_data
            
        except Exception as e:
            logger_obj.error(f"Error in data balancing: {e}")
            raise CustomException(f"Data balancing failed: {e}")
        
    def select_features(self, df: pd.DataFrame):
        try:
            logger_obj.info("[DataProcessor] : Starting feature selection using RandomForestClassifier")
            X = df.drop(columns=['booking_status'])
            y = df['booking_status']
            
            model = RandomForestClassifier(random_state=42)
            model.fit(X,y)
            
            feature_importances = model.feature_importances_
            feature_importances_df = pd.DataFrame({
                'Feature': X.columns,
                'Importance': feature_importances
            })
            
            most_effect_features = feature_importances_df.sort_values(by="Importance", ascending=False)
            num_of_fearures_to_select = self.config.get("num_of_fearures_to_select", 10)
            top_features = most_effect_features['Feature'].head(num_of_fearures_to_select).values
            logger_obj.info(f"[DataProcessor] : Top {num_of_fearures_to_select} features selected: {top_features}")
            
            top_features_with_data = df[top_features.tolist() + ['booking_status']]
            logger_obj.info("[DataProcessor] : Feature selection completed.")
            return top_features_with_data
        except Exception as e:
            logger_obj.error(f"Error in feature selection: {e}")
            raise CustomException(f"Feature selection failed: {e}")
        
    def save_processed_data(self, df: pd.DataFrame, file_path: str):
        try:
            logger_obj.info(f"[DataProcessor] : Saving processed data to {file_path}")
            
            df.to_csv(file_path, index=False)
            
            logger_obj.info(f"[DataProcessor] : Processed data saved successfully at {file_path}")
        except Exception as e:
            logger_obj.error(f"Error saving processed data to {file_path}: {e}")
            raise CustomException(f"Saving processed data failed: {e}")
        
    def process(self):
        try:
            # Load data
            logger_obj.info("[DataProcessor] : Loading data from RAW directory")
            train_data = load_data(self.train_path)
            test_data = load_data(self.test_path)
            
            train_data = self.process_data(train_data)
            test_data = self.process_data(test_data)
            
            train_data = self.balance_data(train_data)
            test_data = self.balance_data(test_data)
            
            train_data = self.select_features(train_data)
            test_data = test_data[train_data.columns]
            
            self.save_processed_data(train_data, PROCESSED_TRAIN_DATA_PATH)
            self.save_processed_data(test_data, PROCESSED_TEST_DATA_PATH)
            
            logger_obj.info("[DataProcessor] : Data processing pipeline completed successfully.")
        except Exception as e:
            logger_obj.error(f"Error in data processing pipeline: {e}")
            raise CustomException(f"Data processing pipeline failed: {e}")
        
        
if __name__ == "__main__":
    data_processor = DataProcessor(
        config_path=CONFIG_PATH,
        train_path=TRAIN_DATA_PATH,
        test_path=TEST_DATA_PATH,
        processed_dir=DATA_PROCESSING_DIR
    )
    data_processor.process()