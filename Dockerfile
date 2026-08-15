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
COPY requirements/ /tmp/requirements/


# ------------------------------
# Copy Deployment Scripts
# ------------------------------
COPY deployment/ /deployment/

RUN chmod +x /deployment/scripts/*.sh

# ------------------------------
# Install Python Requirements
# ------------------------------
RUN pip install --upgrade pip \
    && pip install -r /tmp/requirements/production.txt


# ------------------------------
# Copy Project
# ------------------------------
COPY onlineshop/ .

RUN mkdir -p \
    /static_root \
    /media_root \
    /logs

# ------------------------------
# Expose Port
# ------------------------------
EXPOSE 8000

# --------------------------------------------------
# Entrypoint
# --------------------------------------------------
ENTRYPOINT ["/deployment/scripts/entrypoint.sh"]

# ------------------------------
# Default Command
# ------------------------------
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]