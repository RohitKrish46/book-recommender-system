from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class DataIngestionConfig:
    kaggle_dataset_name: str
    raw_data_dir: str
    ingested_data_dir: str