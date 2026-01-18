import os 
import pandas as pd
import joblib
from sklearn.model_selection import RandomizedSearchCV
import lightgbm as lgb
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from scipy.stats import randint

from src.logger import get_logger
from src.custom_exception import CustomException
from config.path_config import *
from config.model_parms import *
from utils.common_functions import load_data, read_yml_file


logger = get_logger(__name__)

class ModelTrainer:
    def __init__(self, train_data_path: Path, test_data_path: Path, model_output_path: Path):
        self.train_path = train_data_path
        self.test_path = test_data_path
        self.model_output = model_output_path
        
        self.parms_distribution = LIGHTGBM_PARAM
        self.random_search_parms = RANDOM_SEAECH_PARAMS
        
    def load_and_split_data(self):
        try:
            logger.info(f"[ModelTrainer] Loading training data from {self.train_path}")
            train_df = load_data(self.train_path)
            
            logger.info(f"[ModelTrainer] Loading testing data from {self.test_path}")
            test_df = load_data(self.test_path)
            
            X_train = train_df.drop("booking_status", axis=1)
            y_train = train_df["booking_status"]
            
            X_test = test_df.drop("booking_status", axis=1)
            y_test = test_df["booking_status"]
            
            logger.info(f"[ModelTrainer] Successfully split data into features and target")
            return X_train, y_train, X_test, y_test
        except Exception as e:
            logger.exception(f"[ModelTrainer] Error in loading and splitting data: {e}")
            raise CustomException("Failed to load and split data", e)
        
    def train_model(self, X_train, y_train):
        try:
            logger.info(f"[ModelTrainer] Initializing LightGBM classifier")
            lgbm_model = lgb.LGBMClassifier(
                random_state=self.random_search_parms['random_state']
            )
            
            logger.info(f"[ModelTrainer] Starting Randomized Search CV for hyperparameter tuning")
            random_search = RandomizedSearchCV(
                estimator=lgbm_model,
                param_distributions=self.parms_distribution,
                n_iter=self.random_search_parms['n_iter'],
                random_state=self.random_search_parms['random_state'],
                cv=self.random_search_parms['cv'],
                verbose=self.random_search_parms['verbose'],
                n_jobs=self.random_search_parms['n_jobs'],
                scoring=self.random_search_parms['scoring']
            )
            
            logger.info(f"[ModelTrainer] Fitting Randomized Search CV")
            random_search.fit(X_train, y_train)
            
            best_params = random_search.best_params_
            logger.info(f"[ModelTrainer] Best hyperparameters found: {best_params}")
            best_model = random_search.best_estimator_
            
            logger.info("[ModelTrainer] Completing model training")
            return best_model
        except Exception as e:
            logger.exception(f"[ModelTrainer] Error in model training: {e}")
            raise CustomException("Failed to train model", e)
        
        
    def evaluate_model(self, model, X_test, y_test) -> pd.DataFrame:
        try:
            logger.info(f"[ModelTrainer] Evaluating model performance on test data")
            y_pred = model.predict(X_test)
            
            accuracy = accuracy_score(y_pred=y_pred, y_true=y_test)
            logger.info(f"[ModelTrainer] Accuracy: {accuracy}")
            precision = precision_score(y_pred=y_pred, y_true=y_test)
            logger.info(f"[ModelTrainer] Precision: {precision}")
            recall = recall_score(y_pred=y_pred, y_true=y_test)
            logger.info(f"[ModelTrainer] Recall: {recall}")
            f1 = f1_score(y_pred=y_pred, y_true=y_test)
            logger.info(f"[ModelTrainer] F1 Score: {f1}")
            
            metrics_df = pd.DataFrame([{
                "accuracy": accuracy,
                "precision": precision,
                "recall": recall,
                "f1_score": f1
            }])
            
            return metrics_df
        except Exception as e:
            logger.exception(f"[ModelTrainer] Error in model evaluation: {e}")
            raise CustomException("Failed to evaluate model", e)
        
    def save_model(self, model) -> None:
        try:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(self.model_output), exist_ok=True)
            
            logger.info(f"[ModelTrainer] Saving model ...")
            joblib.dump(model, self.model_output)
            logger.info(f"[ModelTrainer] Model saved at {self.model_output}")
        except Exception as e:
            logger.exception(f"[ModelTrainer] Error in saving model: {e}")
            raise CustomException("Failed to save model", e)
        
    def run(self):
        try:
            logger.info(f"[ModelTrainer] Starting model training pipeline")
            X_train, y_train, X_test, y_test = self.load_and_split_data()
            model = self.train_model(X_train, y_train)
            metrics_df = self.evaluate_model(model, X_test, y_test)
            self.save_model(model)
            
            logger.info(f"[ModelTrainer] Model training pipeline completed successfully")
        except Exception as e:
            logger.exception(f"[ModelTrainer] Error in model training pipeline: {e}")
            raise CustomException("Model training pipeline failed", e)
        
if __name__ == "__main__":
    trainer = ModelTrainer(
        train_data_path=PROCESSED_TRAIN_DATA_PATH,
        test_data_path=PROCESSED_TEST_DATA_PATH,
        model_output_path=MODEL_OUTPUT_PATH
    )
    trainer.run()
    
            
             
            