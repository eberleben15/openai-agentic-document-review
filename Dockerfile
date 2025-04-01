FROM python:3.11-slim

WORKDIR /app

# Install essential build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1-mesa-glx \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy all project contents correctly
COPY src/ ./src/
COPY documents/ ./documents/
COPY .env ./

# Ensure the directory structure aligns exactly
CMD ["python", "src/main.py"]