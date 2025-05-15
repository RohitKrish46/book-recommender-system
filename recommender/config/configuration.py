import os
import sys
from recommender.logger.log import logging
from recommender.utils.load_yaml import read_yaml_file
from recommender.exception.exception_handler import AppException
from recommender.entity.config_entity import DataIngestionConfig, DataValidationConfig, DataTransformationConfig, ModelTrainerConfig, ModelRecommendationConfig
from recommender.constants import CONFIG_FILE_PATH

class AppConfiguration:
    """
    This class handles the configuration settings for the application.
    
    Attributes:
        config_file_path (str): Path to the configuration file.
        
    Methods:
        __init__(self, config_file_path: str): Initializes the configuration object.
        get_config(self) -> dict: Returns the configuration settings as a dictionary.
    """
    
    def __init__(self, config_file_path: str = CONFIG_FILE_PATH) -> None:
        """Initialize the AppConfiguration with a given config file path."""
        try:
            self.config_info = read_yaml_file(file_path=config_file_path)
        except Exception as e:
            raise AppException(e, sys) from e
        #logging.info(f"Configuration file loaded from: {config_file_path}")

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        try:
            # get the config dict
            data_ingestion_config = self.config_info['data_ingestion_config']

            # base directory paths
            artifacts_dir = self.config_info['artifacts_config']['artifacts_dir']
            dataset_dir = data_ingestion_config['dataset_dir']
            kaggle_dataset_name = data_ingestion_config['dataset_name']
            ingested_dir = data_ingestion_config['ingested_dir']
            raw_dir = data_ingestion_config['raw_data_dir']

            # nested directory paths
            ingested_data_dir = os.path.join(artifacts_dir, dataset_dir, ingested_dir)
            raw_data_dir = os.path.join(artifacts_dir, dataset_dir, raw_dir)

            response = DataIngestionConfig(
                kaggle_dataset_name = kaggle_dataset_name,
                raw_data_dir = raw_data_dir,
                ingested_data_dir = ingested_data_dir,
            )
            logging.info("Data Ingestion Config Loaded")
            return response
        
        except Exception as e:
            raise AppException(e, sys) from e
        
    def get_data_validation_config(self) -> DataValidationConfig:
        try:
            # get the config dict 
            data_validation_config = self.config_info['data_validation_config']
            data_ingestion_config = self.config_info['data_ingestion_config']

            # base directory paths
            artifacts_dir = self.config_info['artifacts_config']['artifacts_dir']
            dataset_dir = data_ingestion_config['dataset_dir']
            serialized_dir = data_validation_config['serialized_objects_dir']
            ingested_dir = data_ingestion_config['ingested_dir']
            clean_dir = data_validation_config['clean_data_dir']

            # csv file paths
            books_csv_file = data_validation_config['books_csv_file']
            ratings_csv_file = data_validation_config['ratings_csv_file']

            # nested directory paths
            serialized_objects_dir = os.path.join(artifacts_dir, serialized_dir)
            clean_data_dir = os.path.join(artifacts_dir, dataset_dir, clean_dir)

            # nested csv file paths
            books_csv_file_path = os.path.join(artifacts_dir, dataset_dir, ingested_dir, books_csv_file)
            ratings_csv_file_path = os.path.join(artifacts_dir, dataset_dir, ingested_dir, ratings_csv_file)


            response = DataValidationConfig(
                clean_data_dir = clean_data_dir,
                serialized_objects_dir = serialized_objects_dir,
                books_csv_file = books_csv_file_path,
                ratings_csv_file = ratings_csv_file_path,
            )
            logging.info("Data Validation Config Loaded")
            return response
        
        except Exception as e:
            raise AppException(e, sys) from e
        
    def get_data_transformation_config(self) -> DataTransformationConfig:
        try:
            # get the config dict 
            data_transformation_config = self.config_info['data_transformation_config']
            data_validation_config = self.config_info['data_validation_config']
            data_ingestion_config = self.config_info['data_ingestion_config']

            # base directory paths
            artifacts_dir = self.config_info['artifacts_config']['artifacts_dir']
            dataset_dir = data_ingestion_config['dataset_dir']
            transformed_dir = data_transformation_config['transformed_data_dir']
            clean_dir = data_validation_config['clean_data_dir']

            # csv file path
            clean_data_csv = 'clean_data.csv'

            # nested directory paths
            clean_data_file_path = os.path.join(artifacts_dir, dataset_dir, clean_dir, clean_data_csv)
            transformed_data_dir = os.path.join(artifacts_dir, dataset_dir, transformed_dir)

            response = DataTransformationConfig(
                clean_data_file_path = clean_data_file_path,
                transformed_data_dir = transformed_data_dir,
            )
            logging.info("Data Transformation Config Loaded")
            return response
        
        except Exception as e:
            raise AppException(e, sys) from e
        
    def get_model_trainer_config(self) -> ModelTrainerConfig:
        try:
            # get the config dict 
            model_trainer_config = self.config_info['model_trainer_config']
            data_transformation_config = self.config_info['data_transformation_config']
            data_ingestion_config = self.config_info['data_ingestion_config']
            dataset_dir = data_ingestion_config['dataset_dir']

            # base directory paths
            artifacts_dir = self.config_info['artifacts_config']['artifacts_dir']
            models_dir = model_trainer_config['trained_model_dir']
            transformed_data_dir = data_transformation_config['transformed_data_dir']

            # model file name
            trained_model_name = model_trainer_config['trained_model_name']

            # transformed data file name
            transformed_data_file = 'transformed_data.pkl'

            # nested directory paths
            transformed_data_file_dir = os.path.join(artifacts_dir, dataset_dir, transformed_data_dir, transformed_data_file)
            trained_model_dir = os.path.join(artifacts_dir, models_dir)

            response = ModelTrainerConfig(
                transformed_data_file_dir = transformed_data_file_dir,
                trained_model_dir = trained_model_dir,
                trained_model_name = trained_model_name
            )

            logging.info("Model Trainer Config Loaded")
            return response

        except Exception as e:
            raise AppException(e, sys) from e
        
    def get_recommendation_config(self) -> ModelRecommendationConfig:
        try:
            # get the config dict
            model_trainer_config = self.config_info['model_trainer_config']
            data_validation_config = self.config_info['data_validation_config']

            # base directory paths
            artifacts_dir = self.config_info['artifacts_config']['artifacts_dir']
            serialized_objects_dir = data_validation_config['serialized_objects_dir']
            model_dir = model_trainer_config['trained_model_dir']
            # model file name
            trained_model_name = model_trainer_config['trained_model_name']
                    
            # serialized objects file names
            book_name_serialized_objects = os.path.join(artifacts_dir, serialized_objects_dir, 'book_names.pkl')
            book_pivot_serialized_objects = os.path.join(artifacts_dir, serialized_objects_dir, 'book_pivot.pkl')
            final_rating_serialized_objects = os.path.join(artifacts_dir, serialized_objects_dir, 'final_rating.pkl')
            
            # nested directory paths
            trained_model_dir = os.path.join(artifacts_dir, model_dir)

            # trained model file path
            trained_model_path = os.path.join(trained_model_dir,trained_model_name)
          
            response = ModelRecommendationConfig(
                book_name_serialized_objects = book_name_serialized_objects,
                book_pivot_serialized_objects = book_pivot_serialized_objects,
                final_rating_serialized_objects = final_rating_serialized_objects,
                trained_model_path = trained_model_path
            )

            logging.info("Model Recommendation Config Loaded")
            return response

        except Exception as e:
            raise AppException(e, sys) from e
            