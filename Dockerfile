# ============================================
# Multi-stage Docker build for VulnTrack Backend
# ============================================

# ============================================
# Stage 1: Base Python Environment
# ============================================
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# ============================================
# Stage 2: Poetry Dependencies
# ============================================
FROM base as poetry

# Install Poetry
ENV POETRY_HOME="/opt/poetry" \
    POETRY_VERSION=1.7.1
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="$POETRY_HOME/bin:$PATH"

# Set work directory
WORKDIR /app

# Copy Poetry files
COPY pyproject.toml poetry.lock ./

# Configure Poetry and install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --only=main --no-interaction --no-ansi

# ============================================
# Stage 3: Development Environment
# ============================================
FROM poetry as development

# Install development dependencies
RUN poetry install --with dev --no-interaction --no-ansi

# Copy application code
COPY . .

# Create non-root user
RUN groupadd -r vulntrack && useradd -r -g vulntrack vulntrack
RUN chown -R vulntrack:vulntrack /app
USER vulntrack

# Expose port
EXPOSE 8000

# Development command
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# ============================================
# Stage 4: Production Environment
# ============================================
FROM base as production

# Copy installed packages from poetry stage
COPY --from=poetry /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=poetry /usr/local/bin /usr/local/bin

# Set work directory
WORKDIR /app

# Copy application code
COPY app/ ./app/
COPY alembic/ ./alembic/
COPY alembic.ini .
COPY pyproject.toml .

# Create non-root user
RUN groupadd -r vulntrack && useradd -r -g vulntrack vulntrack

# Create necessary directories and set permissions
RUN mkdir -p /app/logs /app/data \
    && chown -R vulntrack:vulntrack /app

# Add build args for metadata
ARG VERSION=unknown
ARG BUILD_DATE=unknown
ARG VCS_REF=unknown

# Add metadata labels
LABEL org.opencontainers.image.title="VulnTrack Backend" \
      org.opencontainers.image.description="Advanced Device Vulnerability Management System" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.created="${BUILD_DATE}" \
      org.opencontainers.image.revision="${VCS_REF}" \
      org.opencontainers.image.source="https://github.com/vulntrack/vulntrack-backend" \
      org.opencontainers.image.licenses="MIT" \
      org.opencontainers.image.vendor="VulnTrack"

# Switch to non-root user
USER vulntrack

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Expose port
EXPOSE 8000

# Production command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]

# ============================================
# Stage 5: Testing Environment
# ============================================
FROM development as testing

# Install additional testing tools
RUN poetry install --with dev,test --no-interaction --no-ansi

# Copy test files
COPY tests/ ./tests/

# Run tests
CMD ["poetry", "run", "pytest", "tests/", "-v", "--cov=app"]
