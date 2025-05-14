import os
import sys
from recommender.logger.log import logging
from recommender.utils.load_yaml import read_yaml_file
from recommender.exception.exception_handler import AppException
from recommender.entity.config_entity import DataIngestionConfig, DataValidationConfig
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
        logging.info(f"Configuration file loaded from: {config_file_path}")

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

            # nested directory paths
            serialized_objects_dir = os.path.join(artifacts_dir, dataset_dir, serialized_dir)
            clean_data_dir = os.path.join(artifacts_dir, dataset_dir, clean_dir)

            # csv file paths
            books_csv_file = os.path.join(artifacts_dir, dataset_dir, ingested_dir)
            ratings_csv_file = os.path.join(artifacts_dir, dataset_dir, ingested_dir)


            response = DataValidationConfig(
                clean_data_dir = clean_data_dir,
                serialized_objects_dir = serialized_objects_dir,
                books_csv_file = books_csv_file,
                ratings_csv_file = ratings_csv_file,
            )
            logging.info("Data Validation Config Loaded")
            return response
        
        except Exception as e:
            raise AppException(e, sys) from e