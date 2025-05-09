FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y \
    git \
    curl \
    build-essential \
    libxml2-dev \
    libxslt1-dev \
    libjpeg-dev \
    zlib1g-dev \
    python3-dev \
    libffi-dev \
    libssl-dev

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

RUN python -m textblob.download_corpora

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

CMD ["bash", "-c", "ollama serve & sleep 5 && python main.py"]