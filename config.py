import os

from sqlalchemy import create_engine

class Config(object):
    SECRET_KEY = "ClaveSecreta"
    SESSION_COOKIE_SECURE = False

class DevelopmentConfig(Config):
    DEBUG = True
    USERDB = 'root'
    CONTRASENIADB = 'cOpernico07#'
    SQLALCHEMY_DARABASE_URI = 'mysql+pymysql://'+USERDB+':'+CONTRASENIADB+'@127.0.0.1/bdidgs801'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

