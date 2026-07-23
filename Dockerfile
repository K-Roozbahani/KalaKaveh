# ------------------------------
# Base Image
# ------------------------------
FROM python:3.14-slim

# ------------------------------
# Environment
# ------------------------------
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

# ------------------------------
# Work Directory
# ------------------------------
WORKDIR /app

# ------------------------------
# System Dependencies
# ------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# ------------------------------
# Install Python Requirements
# ------------------------------
COPY requirements/ ./requirements/

RUN pip install --upgrade pip \
    && pip install -r requirements/production.txt

# ------------------------------
# Copy Project
# ------------------------------
COPY onlineshop/ .

# ------------------------------
# Expose Port
# ------------------------------
EXPOSE 8000

# ------------------------------
# Default Command
# ------------------------------
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]