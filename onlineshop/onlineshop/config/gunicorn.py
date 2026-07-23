"""
تنظیمات Gunicorn پروژه
"""
from pathlib import Path

from environ import Env

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

env = Env()

env.read_env(str(BASE_DIR / ".env"))
# ------------------------------------------------------------------
# Server
# ------------------------------------------------------------------

bind = env(
    "GUNICORN_BIND",
    default="0.0.0.0:8000",
)

# ------------------------------------------------------------------
# Workers
# ------------------------------------------------------------------

workers = env.int(
    "GUNICORN_WORKERS",
    default=2,
)

# ------------------------------------------------------------------
# Timeout
# ------------------------------------------------------------------

timeout = env.int(
    "GUNICORN_TIMEOUT",
    default=60,
)

graceful_timeout = env.int(
    "GUNICORN_GRACEFUL_TIMEOUT",
    default=30,
)

keepalive = env.int(
    "GUNICORN_KEEPALIVE",
    default=5,
)

# ------------------------------------------------------------------
# Logging
# ------------------------------------------------------------------

accesslog = "-"

errorlog = "-"

loglevel = env(
    "GUNICORN_LOG_LEVEL",
    default="info",
)

capture_output = True

# ------------------------------------------------------------------
# Worker Recycling
# ------------------------------------------------------------------

max_requests = env.int(
    "GUNICORN_MAX_REQUESTS",
    default=1000,
)

max_requests_jitter = env.int(
    "GUNICORN_MAX_REQUESTS_JITTER",
    default=100,
)