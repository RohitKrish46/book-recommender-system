import os
import sys
from recommender.logger.log import logging
from recommender.utils.load_yaml import read_yaml_file
from recommender.exception.exception_handler import AppException
from recommender.entity.config_entity import DataIngestionConfig
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
            data_ingestion_config = self.config_info['data_ingestion_config']
            artifacts_dir = self.config_info['artifacts_config']['artifacts_dir']
            dataset_dir = data_ingestion_config['dataset_dir']

            ingested_data_dir = os.path.join(artifacts_dir, dataset_dir, data_ingestion_config['ingested_dir'])
            raw_data_dir = os.path.join(artifacts_dir, dataset_dir, data_ingestion_config['raw_data_dir'])

            response = DataIngestionConfig(
                dataset_download_url = data_ingestion_config['dataset_download_url'],
                raw_data_dir = raw_data_dir,
                ingested_dir = ingested_data_dir
            )
            logging.info(f"Data Ingestion Config: {response}")
            return response
        
        except Exception as e:
            raise AppException(e, sys) from e