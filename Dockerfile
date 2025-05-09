FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y curl build-essential && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh
ENV PATH="/root/.ollama/bin:${PATH}"

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose Ollama's default port
EXPOSE 11434

# Start Ollama server when the container runs
CMD ["ollama", "serve"]