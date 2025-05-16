# Book Recommender System

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/Docker-28.1.1-blue?logo=docker)](https://hub.docker.com/r/yourusername/your-repo)
[![AWS EC2](https://img.shields.io/badge/AWS_EC2-Deployed-yellow?logo=amazon-ec2)](https://aws.amazon.com/ec2)
[![docker pulls](https://img.shields.io/docker/pulls/rokrr/bookapp?logo=docker&label=docker-pulls)](https://hub.docker.com/r/rokrr/bookapp)
[![Streamlit 1.45.1+](https://img.shields.io/badge/Streamlit-v1.45.1%2B-FF4B4B?logo=streamlit)](https://your-url)

Book Recommender System is a modular and extensible book recommendation engine, featuring a custom training pipeline, robust logging and exception handling, and an interactive Streamlit interface for real-time book recommendations. The project is fully deployed on AWS EC2, providing a scalable, production-ready environment for live usage and demonstrations. Designed with clean architecture and best practices, it supports both experimentation and real-world deployment.

## Table of Contents
- [Overview](#overview)

- [Features](#features)

- [Architecture and Workflow](#architecture-and-workflow)

- [AWS EC2 Deployment Guide](#aws-ec2-deployment-guide)

- [Usage](#usage)

- [Application Screenshots](#application-screenshots)

- [Internal Conventions](#internal-conventions)

- [Folder Structure](#folder-structure)

- [Technologies Stack](#technologies-stack)

- [Future Improvements](#future-improvements)


## Overview

This system recommends books based on collaborative filtering. It includes:

- A multi-stage pipeline for training the recommender.

- A Streamlit UI for training the model and getting recommendations.

- Modular design for easy extension and experimentation.

All components (data ingestion, transformation, training, and inference) are wrapped with logging and exception handling for production readiness.

## Features
- **Book Recommendations** using Nearest Neighbors on user ratings.

- **Trainable Engine**: Execute an end-to-end pipeline for data ingestion to model training.

- **Modular Design**: Add or replace pipeline components independently.

- **Robust Logging and Error Management** with centralized log tracking.

- **Interactive UI using Streamlit** for recommendation queries and pipeline triggers.

- **Model Persistence** with pickle-based artifact storage and reusability.

## Architecture and Workflow

### Book Recommendation Architecture
![image](https://github.com/user-attachments/assets/4727923d-08bd-45c8-bce7-913a66c91e45)



### Model Training Pipeline Workflow
![image](https://github.com/user-attachments/assets/363571aa-4a60-4277-b709-838940b160d7)

### Pipeline Workflow

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


## AWS EC2 Deployment Guide

### Deploying the Streamlit App on AWS EC2

**1. Launch an EC2 Instance**
   - Log in to your AWS Console.
   - Launch/Create a Ubuntu-based EC2 instance.
   - Configure port 8501 to be open in the security group (for Streamlit access).

**2. Connect to the EC2 Instance from inside the AWS console**

**3. Set Up Docker**
```
# Update system and install dependencies
sudo apt-get update -y
sudo apt-get upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu
newgrp docker
```
**4. Deploy our project**
```
# Clone your project (replace with your repo)
git clone https://github.com/RohitKrish46/book-recommender-system.git
cd book-recommender-system

# Build and run the Docker image (adviseable to use your docker user_id -> docker build -t {username}/bookapp:latest .)
docker build -t rokrr/bookapp:latest .
docker run -d -p 8501:8501 rokrr/bookapp
```
**5. Access the App**
Open your browser and navigate to:
`http://<EC2_PUBLIC_IP>:8501`

 ### Additional commands (Optional)

**1. Stop/Remove Containers**
```
docker stop <container_id>
docker rm $(docker ps -a -q)
```
**2. Push/Pull Docker Image**
```
docker login
docker push entbappy/stapp:latest   # Push to registry
docker pull entbappy/stapp:latest    # Pull latest image
```

## Usage

### Initial Setup Using UV (Recommended)

**1. Install UV** (if not already installed):
  ```
  # bash
  pipx install uv

  # Using curl
  curl -LsSf https://astral.sh/uv/install.sh | sh

  # Or with pip
  python -m pip install uv
  ```
**2. Create & activate a virtual environment**:
```
uv venv <virtual-env-name>
```
**3. Activate Envoirnment**
```
# Linux/macOS
source <virtual-env-name>/bin/activate

# Windows
.\<virtual-env-name>\Scripts\Activate
```
**4. Clone this repo**
```
git clone https://github.com/RohitKrish46/book-recommender-system.git
```
Now just get all your content into the uv managed repo

**5. Install Dependencies**:
```
uv pip install -r requirements.txt
```

### Train the Recommendation Engine
```
python main.py
```
This triggers the entire training pipeline:
   - Ingests and validates data
   - Builds pivot tables
   - Trains Nearest Neighbors model
   - Saves trained artifacts for inference

### Run the Streamlit App
```
streamlit run app.py
```
Visit [http://localhost:8501](http://localhost:8501) to interact with the UI.

Streamlit UI Features:
   - Train Engine: Run training from the UI
   - Get Recommendations: Type a book name to see similar recommendations
   - Cover Images: Displays book covers alongside titles

## Application Screenshots
1. **Home page**:  A page with an introduction to the app
![image](https://github.com/user-attachments/assets/a8da13d8-c21b-4039-ba14-098c5de11cbb)
2. **Train Recommender system**: Click the button to freshly train the recommender system 
![image](https://github.com/user-attachments/assets/a59e5c36-2b15-49aa-8579-de9e007f2b81)
3. **Get similar recommendations**: Choose a book you like
![image](https://github.com/user-attachments/assets/8568c661-f70e-4ddc-a9d7-212d37c4302d)
4. **About this app**
![image](https://github.com/user-attachments/assets/83ee63c8-31a1-409d-8f22-c3eb9bebcbd9)


## Internal Conventions

- **Logging:**  
  Uses `recommender.logger.log` for consistent logging across modules.

- **Exception Handling:**  
  All major operations are wrapped in try/except blocks and raise `AppException` for unified error management.

- **Configuration:**  
  Uses an `AppConfiguration` object to manage paths for models and serialized objects.

- **Artifacts:**  
  Trained models and serialized data (e.g., pivot tables, ratings) are loaded and saved using `pickle`.

## Folder Structure

```
book-recommender-system/
├── app.py                           # Streamlit app interface
├── main.py                          # Training pipeline trigger
├── recommender/
│   ├── components/                  # All modular pipeline steps
│   │   ├── data_ingestion.py
│   │   ├── data_validation.py
│   │   ├── data_transformation.py
│   │   └── model_training.py
│   ├── constants/
│   │   └── __init__.py              # constant configs
│   ├── entity/
│   │   └── config_entity.py         # Dataclass for configs
│   ├── exception/
│   │   └── exception.py             # AppException class
│   ├── logger/
│   │   └── log.py                   # AppLogger class
│   ├── pipelines/
│   │   └── training_pipeline.py     # Orchestrates all components
│   └── utils/
│       └── load_yaml.py             # AppConfiguration manager
├── artifacts/                     
│   ├── dataset/                 
│   │   ├── clean_data/              # Preprocessed data
│   │   ├── ingested_data/           # Extracted csv's
│   │   ├── raw_data/                # Dataset's raw zip file
│   │   └── transformed_data/        # Pivot files
│   ├── serialized_objects/          # Pickle files
│   ├── trained_model/               # Stores trained model
├── config/
│   │   ├── config.yaml/             # Main Configuration
├── templates/
│   │   ├── book_names.pkl/          # Book Names for Streamlit
├── Dockerfile                       # Docker Image Config
├── requirements.txt
└── README.md

```

## Technologies Stack

**Programming Language** 

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

**Machine Learning**  

![Scikit-learn](https://img.shields.io/badge/Scikit--learn-ff9933?style=for-the-badge&logo=scikit-learn&logoColor=white)
![SciPy](https://img.shields.io/badge/SciPy-8CAAE6?style=for-the-badge&logo=scipy&logoColor=white)

**Data Manipulation & Visualization** 

![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)
![Seaborn](https://img.shields.io/badge/Seaborn-7db0bc?style=for-the-badge&logo=chartdotjs&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-11557C?style=for-the-badge&logo=plotly&logoColor=white)

**Deployment & Web Framework**  

![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![AWS EC2](https://img.shields.io/badge/AWS%20EC2-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)

**Package Manager**

![uv](https://img.shields.io/badge/uv-311f3a?style=for-the-badge&logo=zap&logoColor=white)

## Future Improvements
Below are some enhancements planned for future versions:

- **Hybrid Recommendation Models**: Combine collaborative filtering with content-based filtering using book metadata (genres, authors, descriptions, etc.) for improved personalization.

- **Incorporate NLP Models**: Integrate transformer-based models like BERT to analyze book descriptions or user reviews for semantic recommendations.

- **CI/CD Integration**: Set up automated testing and deployment workflows using GitHub Actions or similar tools.

- **Graph-based Recommendation**: Explore knowledge graph embeddings or user-book interaction graphs to enhance recommendation diversity and explainability.
