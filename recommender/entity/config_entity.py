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