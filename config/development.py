from jump2.config.default import *

# BASE_DIR = '/home/hshkuber/jump2/'
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pro2.db'))

SQLALCHEMY_TRACk_MODIFICATIONS = False

SECRET_KEY = "dev1234"


