import os
import sys
import zipfile
import pandas as pd
from dotenv import load_dotenv
from abc import ABC, abstractmethod
from kaggle.api.kaggle_api_extended import KaggleApi
import logging
from recommender.exception.exception_handler import AppException
from recommender.config.configuration import AppConfiguration

load_dotenv() # Load environment variables from .env file

# Abstract class for data ingestion
class DataIngestion(ABC):
    @abstractmethod
    def ingest_data(self, file_path: str) -> pd.DataFrame:
        pass


# Concrete class for ingesting data from a ZIP file
class ZipDataIngestion(DataIngestion):
    def __init__(self, app_config=AppConfiguration()):
        try:
            self.data_ingestion_config = app_config.get_data_ingestion_config()
            logging.info(f"{'='*20}Data Ingestion Initialized{'='*20}")
        except Exception as e:
            raise AppException(e, sys) from e

    def download_data(self) -> str:
        """Downloads the dataset from Kaggle and returns the zip file path"""
        try:
            # Load Kaggle credentials from environment variables
            username = os.getenv("KAGGLE_USERNAME")
            key = os.getenv("KAGGLE_KEY")
            
            if not username or not key:
                raise ValueError("Kaggle credentials not found in environment variables.")

            dataset_name = self.data_ingestion_config.kaggle_dataset_name
            zip_download_dir = self.data_ingestion_config.raw_data_dir
            os.makedirs(zip_download_dir, exist_ok=True)

            zip_file_path = os.path.join(zip_download_dir, 'bookrecommendation.zip')

            # ✅ Check if the zip file already exists
            if os.path.exists(zip_file_path):
                logging.info(f"Zip file already exists at {zip_file_path}. Skipping download.")
                return zip_file_path

            api = KaggleApi()
            api.authenticate()

            logging.info(f"Downloading dataset {dataset_name} to {zip_download_dir}")
            api.dataset_download_files(dataset=dataset_name, path=zip_download_dir, quiet=False)

            if not os.path.exists(zip_file_path):
                raise FileNotFoundError(f"Zip file not found at: {zip_file_path}")

            logging.info(f"Downloaded zip to {zip_file_path}")
            return zip_file_path
        except Exception as e:
            raise AppException(e, sys) from e

    def ingest_data(self, file_path: str) -> pd.DataFrame:
        """Extracts ZIP and loads CSV as a pandas DataFrame"""
        try:
            if not file_path.endswith('.zip'):
                raise ValueError("The provided file is not a .zip file.")

            ingested_dir = self.data_ingestion_config.ingested_data_dir
            if os.path.exists(ingested_dir):
                for file in os.listdir(ingested_dir):
                    os.remove(os.path.join(ingested_dir, file))
                os.rmdir(ingested_dir)

            os.makedirs(ingested_dir, exist_ok=True)
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(ingested_dir)

            logging.info(f"Extracted csv files from zip file: {file_path} into {ingested_dir}")

            csv_files = [f for f in os.listdir(ingested_dir) if f.endswith('.csv')]
            if len(csv_files) == 0:
                raise FileNotFoundError("No .csv file found in the extracted data.")
            if len(csv_files) > 3:
                raise ValueError("More than one .csv file found in the extracted data.")

            logging.info(f"{'='*20}Data ingestion completed{'='*20}")

        except Exception as e:
            raise AppException(e, sys) from e


# Factory class for Data Ingestors
class DataIngestionFactory:
    @staticmethod
    def get_data_ingestor(file_extension: str) -> DataIngestion:
        if file_extension.endswith('.zip'):
            return ZipDataIngestion()
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")


