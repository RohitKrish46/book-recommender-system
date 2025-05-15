import sys
from recommender.components.data_ingestion import DataIngestionFactory, ZipDataIngestion
from recommender.components.data_validation import DataValidation
from recommender.components.data_transformation import DataTransformation
from recommender.components.model_training import ModelTrainer
from recommender.exception.exception_handler import AppException
from recommender.logger import log
import logging

class TrainingPipeline:
    def __init__(self):
        pass


    def start_training_pipeline(self):
        # step 1: Data Ingestion
        try:
            # get data ingestor
            data_ingestion = DataIngestionFactory()
            ingestor = data_ingestion.get_data_ingestor()

            # only download if file does not exist
            if isinstance(ingestor, ZipDataIngestion):
                file_path = ingestor.download_data()

            # ingest data
            ingestor.ingest_data(file_path)

        except Exception as e:
            logging.error(f"Error during ingestion: {e}")
            raise AppException(e, sys) from e
        
        # step 2: Data Validation / Preprocessing
        try:      
            # initiate data reprocess data
            data_validation = DataValidation()
            data_validation.start_data_validation()

        except Exception as e:
            logging.error(f"Error during data validation: {e}")
            raise AppException(e, sys) from e
        
        # step 3: Data Transformation
        try:
            # initiate data transformation
            data_transformation = DataTransformation()
            data_transformation.initiate_data_transformation()

        except Exception as e:
            logging.error(f"Error during data transformation: {e}")
            raise AppException(e, sys) from e
        
        # step 4: Model Training
        try:
            # initiate model training
            model_trainier = ModelTrainer()
            model_trainier.initiate_model_trainer()

        except Exception as e:
            logging.error(f"Error during model training: {e}")
            raise AppException(e, sys) from e


            