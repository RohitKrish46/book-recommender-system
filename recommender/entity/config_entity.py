from dataclasses import dataclass

@dataclass(frozen=True)
class DataIngestionConfig:
    kaggle_dataset_name: str
    raw_data_dir: str
    ingested_data_dir: str

@dataclass(frozen=True)
class DataValidationConfig:
  clean_data_dir: str
  serialized_objects_dir: str
  books_csv_file: str
  ratings_csv_file: str

@dataclass(frozen=True)
class DataTransformationConfig:
  clean_data_file_path: str
  transformed_data_dir: str

@dataclass(frozen=True)
class ModelTrainerConfig:
  transformed_data_file_dir: str
  trained_model_dir: str
  trained_model_name: str

@dataclass(frozen=True)
class ModelRecommendationConfig:
  book_name_serialized_objects: str
  book_pivot_serialized_objects: str
  final_rating_serialized_objects: str
  trained_model_path: str
