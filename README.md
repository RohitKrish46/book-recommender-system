
# Book Recommender System

A modular book recommendation system built in Python, featuring a robust training pipeline and a Streamlit-based recommendation interface.

---

## Overview

This project implements a book recommender system using a multi-stage pipeline. The pipeline handles data ingestion, validation, transformation, and model training. The system is designed for extensibility and reliability, with custom logging and exception handling throughout.

---

## Project Structure

```
book-recommender-system/
│
├── app.py                          # Streamlit app and recommendation logic
├── main.py                         # Entry point for running the training pipeline
├── recommender/
│   ├── pipelines/
│   │   └── training_pipeline.py    # Orchestrates the training pipeline steps
│   ├── components/                 # Data ingestion, validation, transformation, and training modules
│   ├── logger/                     # Logging utilities
│   └── exception/                  # Custom exception handling
└── ...
```

---

## Pipeline Workflow

The training pipeline consists of the following steps:

1. **Data Ingestion:**  
   Downloads and ingests the dataset using a factory pattern. Only downloads if the file does not exist.

2. **Data Validation / Preprocessing:**  
   Validates and preprocesses the ingested data.

3. **Data Transformation:**  
   Transforms the validated data for model training.

4. **Model Training:**  
   Trains the recommendation model and saves the trained model artifact.

Each step is wrapped in exception handling and logs errors using the internal logging system.

---

## Usage

### 1. Train the Recommendation Engine

To run the training pipeline:

```bash
python main.py
```

This will execute all pipeline steps in sequence. Progress and errors are logged.

### 2. Run the Streamlit App

The `app.py` file provides a Streamlit interface for generating book recommendations.

#### Features:
- **Train Engine:** Triggers the training pipeline from the UI.
- **Get Recommendations:** Enter a book name to receive recommendations and cover images.

#### Example usage in code:
```python
rec = Recommendation()
rec.train_engine()  # Trains the pipeline and displays a message
rec.recommendations_engine(selected_books)  # Shows recommended books with images
```

---

## Internal Conventions

- **Logging:**  
  Uses `recommender.logger.log` for consistent logging across modules.

- **Exception Handling:**  
  All major operations are wrapped in try/except blocks and raise `AppException` for unified error management.

- **Configuration:**  
  Uses an `AppConfiguration` object to manage paths for models and serialized objects.

- **Artifacts:**  
  Trained models and serialized data (e.g., pivot tables, ratings) are loaded and saved using `pickle`.

---

## Requirements

- Python 3.x
- streamlit
- numpy
- pickle
- (Other dependencies as required by your components)

Install dependencies with:

```bash
pip install -r requirements.txt
```

---

## Notes

- The pipeline is modular; each stage can be extended or replaced.
- The recommendation engine uses a nearest neighbors model trained on user ratings.
- The Streamlit app displays recommendations with book cover images.

---

## License

This project is for educational and demonstration purposes.

---

For questions or issues, please open an issue in the repository.
