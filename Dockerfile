FROM python:3.10-slim-buster

# Expose the port Streamlit will run on
EXPOSE 8501

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy all files to the working directory
COPY . /app

# Install Python dependencies using pip
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Command to run the application
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]