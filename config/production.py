from jump2.config.default import *

# BASE_DIR = '/home/hshkuber/backend/jump2/'
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pro2.db'))

SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = b'\x07<\xb1\xac\xad\x9dC\xe2\x88t\xe9\xd4=b\xf0\x8d'


