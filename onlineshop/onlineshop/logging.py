"""
تنظیمات Logging پروژه
"""

from pathlib import Path

from environ import Env


env = Env()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# ------------------------------------------------------------------
# Logging Environment Variables
# ------------------------------------------------------------------

LOG_DIR = Path(env("LOG_DIR", default=BASE_DIR / "logs"))
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_LEVEL = env("LOG_LEVEL", default="INFO")
LOG_BACKUP_COUNT = env.int("LOG_BACKUP_COUNT", default=30)
LOG_ROTATE_WHEN = env("LOG_ROTATE_WHEN", default="midnight")
LOG_TO_CONSOLE = env.bool("LOG_TO_CONSOLE", default=True)

# ------------------------------------------------------------------
# Handlers
# ------------------------------------------------------------------

handlers = {
    "activity_file": {
        "class": "logging.handlers.TimedRotatingFileHandler",
        "level": LOG_LEVEL,
        "filename": LOG_DIR / "activity.log",
        "when": LOG_ROTATE_WHEN,
        "backupCount": LOG_BACKUP_COUNT,
        "encoding": "utf-8",
        "delay": True,
        "formatter": "standard",
    },
    "payment_file": {
        "class": "logging.handlers.TimedRotatingFileHandler",
        "level": LOG_LEVEL,
        "filename": LOG_DIR / "payment.log",
        "when": LOG_ROTATE_WHEN,
        "backupCount": LOG_BACKUP_COUNT,
        "encoding": "utf-8",
        "delay": True,
        "formatter": "standard",
    },
    "error_file": {
        "class": "logging.handlers.TimedRotatingFileHandler",
        "level": "ERROR",
        "filename": LOG_DIR / "error.log",
        "when": LOG_ROTATE_WHEN,
        "backupCount": LOG_BACKUP_COUNT,
        "encoding": "utf-8",
        "delay": True,
        "formatter": "error",
    },
}

if LOG_TO_CONSOLE:
    handlers["console"] = {
        "class": "logging.StreamHandler",
        "level": LOG_LEVEL,
        "formatter": "standard",
    }

# ------------------------------------------------------------------
# Loggers
# ------------------------------------------------------------------

activity_handlers = ["activity_file"]
payment_handlers = ["payment_file"]
error_handlers = ["error_file"]

if LOG_TO_CONSOLE:
    activity_handlers.append("console")
    payment_handlers.append("console")
    error_handlers.append("console")

# ------------------------------------------------------------------
# Logging Configuration
# ------------------------------------------------------------------

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "standard": {
            "()": "config.logging.formatters.ProductionFormatter",
            "format": (
                "[%(asctime)s] "
                "%(levelname)-8s "
                "%(message)s"
            ),
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "error": {
            "()": "config.logging.formatters.ProductionFormatter",
            "format": (
                "\n"
                "================================================================================\n"
                "TIME         : %(asctime)s\n"
                "LEVEL        : %(levelname)s\n"
                "LOGGER       : %(name)s\n"
                "PATH         : %(request_path)s\n"
                "METHOD       : %(request_method)s\n"
                "USER         : %(user_id)s\n"
                "VIEW         : %(view)s\n"
                "IP           : %(ip)s\n"
                "FILE         : %(pathname)s\n"
                "FUNCTION     : %(funcName)s\n"
                "LINE         : %(lineno)d\n"
                "MESSAGE      : %(message)s\n"
                "================================================================================"
            ),
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },

    "handlers": handlers,

    "loggers": {
        "activity": {
            "handlers": activity_handlers,
            "level": LOG_LEVEL,
            "propagate": False,
        },
        "payments": {
            "handlers": payment_handlers,
            "level": LOG_LEVEL,
            "propagate": False,
        },
        "error": {
            "handlers": error_handlers,
            "level": "ERROR",
            "propagate": False,
        },
    },

    "root": {
        "handlers": ["console"] if LOG_TO_CONSOLE else [],
        "level": LOG_LEVEL,
    },
}