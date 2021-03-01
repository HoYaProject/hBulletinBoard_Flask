from config.default import *

SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(BASE_DIR, "hbb.db")}'
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = "dev"

SIMPLEMDE_JS_IIFE = True
SIMPLEMDE_USE_CDN = True

MAIL_SERVER = "smtp.gmail.com"
MAIL_PORT = 465
MAIL_USERNAME = ""
MAIL_PASSWORD = ""
MAIL_USE_TLS = False
MAIL_USE_SSL = True
