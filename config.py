import os


class Config:
    """Base config"""
    SECRET_KEY = "OMG-SUPER-SECRET-yawoeN"
    FLASK_APP = "run.py"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProdConfig(Config):
    """Development configuration"""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///webapi.db"


class DevConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///dev_webapi.db"
