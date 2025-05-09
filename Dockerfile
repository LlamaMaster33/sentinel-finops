FROM python:3.10-slim

WORKDIR /app

# Copy only necessary files
COPY requirements.txt .
COPY . .

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git curl libxml2-dev libxslt1-dev \
    libjpeg-dev zlib1g-dev libffi-dev libssl-dev && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python -m textblob.download_corpora

# Install Ollama CLI
RUN curl -fsSL https://ollama.com/install.sh | sh

# Expose Ollama's default port
EXPOSE 11434

# Start Ollama and the main application
CMD ["bash", "-c", "ollama serve & python main.py"]