from config.default import *

SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(BASE_DIR, "hbb.db")}'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = b"\xd3DLYd\x99\x88\xb6\xf6\xcd\xbe\x12j\xcc\x9d\xdb"
