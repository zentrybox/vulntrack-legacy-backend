# Dockerfile para VulnTrack Backend + Celery + Flower
FROM python:3.11-slim

# Evita prompts interactivos
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

WORKDIR /app

# Instala dependencias del sistema
RUN apt-get update && \
    apt-get install -y build-essential gcc && \
    rm -rf /var/lib/apt/lists/*

# Copia requirements y código
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . .

# Variables de entorno por defecto (pueden ser sobreescritas por docker-compose)
ENV SUPABASE_URL=""
ENV SUPABASE_KEY=""
ENV BRAVE_SEARCH_API_KEY=""
ENV BRAVE_SEARCH_BASE_URL=""
ENV GEMINI_API_KEY=""
ENV REDIS_URL="redis://redis:6379/0"

# Comando por defecto: solo API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
