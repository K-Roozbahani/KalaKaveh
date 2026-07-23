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
COPY deployment/scripts/ /deployment/scripts/

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

# ------------------------------
# Expose Port
# ------------------------------
EXPOSE 8000

# ------------------------------
# Default Command
# ------------------------------
ENTRYPOINT ["/deployment/scripts/entrypoint.sh"]

CMD [
    "gunicorn",
    "--config",
    "deployment/gunicorn.conf.py",
    "config.wsgi:application"
]