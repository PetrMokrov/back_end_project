import os

class Config(object):
  SECRET_KEY = os.environ.get('SECRET_KEY') or 'lenin'

  SECRET_SIGN_MSG_KEY = os.environ.get('SECRET_SIGN_MSG_KEY') or 'stalin'