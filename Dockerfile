FROM python:3.13-slim

WORKDIR /app

# Installation des dépendances système si besoin
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copier les dépendances
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copier le projet
COPY . .

# Lancer le bot
CMD ["python", "main.py"]