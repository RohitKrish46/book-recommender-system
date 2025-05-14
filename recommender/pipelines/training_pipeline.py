import sys
from recommender.components.ingest_data import DataIngestionFactory, ZipDataIngestion
from recommender.exception.exception_handler import AppException
from recommender.logger.log import logging
class TrainingPipeline:
    def __init__(self):
        self.data_ingestion = DataIngestionFactory()

    def start_training_pipeline(self):
        # step 1: Data Ingestion
        try:
            # get data ingestor
            ingestor = self.data_ingestion.get_data_ingestor()

            # only download if file does not exist
            if isinstance(ingestor, ZipDataIngestion):
                file_path = ingestor.download_data()

            # ingest data
            ingestor.ingest_data(file_path)

        except Exception as e:
            logging.error(f"Error during ingestion: {e}")
            raise AppException(e, sys) from e
            
            # Step 2: Preprocess data
            # self.data_preprocessing.preprocess_data()
            # Step 3: Train model
            # self.model_training.train_model()
            # Step 4: Evaluate model
            # self.model_evaluation.evaluate_model()

            