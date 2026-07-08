"""
تنظیمات Logging پروژه

این فایل مسئول تنظیم Loggerها، Handlerها و Formatterهای پروژه است.
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,

    # ---------------------------------------------------------
    # Formatter
    # ---------------------------------------------------------
    "formatters": {
        "standard": {
            "format": (
                "[%(asctime)s] "
                "%(levelname)s "
                "%(message)s"
            ),
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "error": {
            "format": (
                "\n"
                "======================================================================\n"
                "TIME      : %(asctime)s\n"
                "LEVEL     : %(levelname)s\n"
                "LOGGER    : %(name)s\n"
                "FILE      : %(pathname)s\n"
                "FUNCTION  : %(funcName)s\n"
                "LINE      : %(lineno)d\n\n"
                "MESSAGE:\n"
                "%(message)s\n"
                "======================================================================"
            ),
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },

    # ---------------------------------------------------------
    # Handlers
    # ---------------------------------------------------------
    "handlers": {

        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "standard",
        },

        "activity_file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "INFO",
            "filename": LOG_DIR / "activity.log",
            "when": "midnight",
            "backupCount": 30,
            "encoding": "utf-8",
            "delay": True,
            "formatter": "standard",
        },

        "payment_file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "INFO",
            "filename": LOG_DIR / "payment.log",
            "when": "midnight",
            "backupCount": 30,
            "encoding": "utf-8",
            "delay": True,
            "formatter": "standard",
        },

        "error_file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "ERROR",
            "filename": LOG_DIR / "error.log",
            "when": "midnight",
            "backupCount": 30,
            "encoding": "utf-8",
            "delay": True,
            "formatter": "error",
        },
    },

    # ---------------------------------------------------------
    # Loggers
    # ---------------------------------------------------------
    "loggers": {

        # ثبت رویدادهای کاربران
        "activity": {
            "handlers": ["activity_file", "console"],
            "level": "INFO",
            "propagate": False,
        },

        # ثبت عملیات پرداخت
        "payments": {
            "handlers": ["payment_file", "console"],
            "level": "INFO",
            "propagate": False,
        },

        # ثبت خطاها
        "error": {
            "handlers": ["error_file", "console"],
            "level": "ERROR",
            "propagate": False,
        },

        # خطاهای خود Django
        "django": {
            "handlers": ["error_file"],
            "level": "ERROR",
            "propagate": False,
        },

    },

    # ---------------------------------------------------------
    # Root Logger
    # ---------------------------------------------------------
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}