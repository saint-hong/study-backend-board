from jump2.config.default import *
from logging.config import dictConfig # error check

# BASE_DIR = '/home/hshkuber/backend/jump2/'
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pro2.db'))

SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = b'\x07<\xb1\xac\xad\x9dC\xe2\x88t\xe9\xd4=b\xf0\x8d'

dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
            }
        },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/jump2.log'),
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
            'formatter': 'default',
            },
        },
    'root': {
        'level': 'INFO',
        'handlers': ['file']
        }
    })
