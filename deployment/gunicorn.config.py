"""
تنظیمات Gunicorn پروژه

این فایل فقط مربوط به Deployment است و
تمام تنظیمات از Environment دریافت می‌شوند.
"""

from environ import Env

env = Env()

# ------------------------------------------------------------------
# Server
# ------------------------------------------------------------------

# آدرس و پورت اجرای Gunicorn
bind = env(
    "GUNICORN_BIND",
    default="0.0.0.0:8000",
)

# ------------------------------------------------------------------
# Workers
# ------------------------------------------------------------------

# تعداد Worker ها
workers = env.int(
    "GUNICORN_WORKERS",
    default=2,
)

# نوع Worker
worker_class = env(
    "GUNICORN_WORKER_CLASS",
    default="gthread",
)

# تعداد Thread هر Worker
threads = env.int(
    "GUNICORN_THREADS",
    default=2,
)

# ------------------------------------------------------------------
# Timeout
# ------------------------------------------------------------------

# حداکثر زمان پردازش هر درخواست
timeout = env.int(
    "GUNICORN_TIMEOUT",
    default=60,
)

# زمان انتظار برای خاموش شدن Worker
graceful_timeout = env.int(
    "GUNICORN_GRACEFUL_TIMEOUT",
    default=30,
)

# مدت نگهداری Connection
keepalive = env.int(
    "GUNICORN_KEEPALIVE",
    default=5,
)

# ------------------------------------------------------------------
# Logging
# ------------------------------------------------------------------

# لاگ‌ها به stdout/stderr ارسال می‌شوند
# تا Docker بتواند آن‌ها را مدیریت کند.
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

# جلوگیری از Memory Leak
max_requests = env.int(
    "GUNICORN_MAX_REQUESTS",
    default=1000,
)

max_requests_jitter = env.int(
    "GUNICORN_MAX_REQUESTS_JITTER",
    default=100,
)

# ------------------------------------------------------------------
# Process
# ------------------------------------------------------------------

# داخل Docker نباید Daemon شود.
daemon = False

# بارگذاری برنامه بعد از ایجاد Worker
preload_app = False

# فایل PID
pidfile = "/tmp/gunicorn.pid"

# استفاده از RAM برای فایل‌های موقت Worker
worker_tmp_dir = "/dev/shm"