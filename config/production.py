from logging.config import dictConfig

from config.default import *

SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(BASE_DIR, "hbb.db")}'
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = b"\xd3DLYd\x99\x88\xb6\xf6\xcd\xbe\x12j\xcc\x9d\xdb"

SIMPLEMDE_JS_IIFE = True
SIMPLEMDE_USE_CDN = True

MAIL_SERVER = "smtp.gmail.com"
MAIL_PORT = 465
MAIL_USERNAME = ""
MAIL_PASSWORD = ""
MAIL_USE_TLS = False
MAIL_USE_SSL = True

dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
            }
        },
        "handlers": {
            "file": {
                "level": "INFO",
                "class": "logging.handlers.RotatingFileHandler",
                "filename": os.path.join(BASE_DIR, "logs/hbb.log"),
                "maxBytes": 1024 * 1024 * 5,
                "backupCount": 5,
                "formatter": "default",
            }
        },
        "root": {"level": "INFO", "handlers": ["file"]},
    }
)
