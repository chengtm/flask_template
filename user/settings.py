# -*- coding: utf-8 -*-
"""Application configuration."""
import os


class Config(object):
    """Base configuration."""
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    BCRYPT_LOG_ROUNDS = 13
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TOKEN_EXPIRATION_TIME = 3600 * 24 * 30

    # Access-Control-Allow-Origin
    ACAO = '*'

    # secret_key
    SECRET_KEY = 'h27z\xee?\x05.1\xf2\xa1\x04Px\x8a\xa1Nsvh\xc3\x7fw\xc5\x80\xb3\xd8\xf7&\x18\xce\xfb'


class ProdConfig(Config):
    """Production configuration."""

    ENV = 'prod'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:@localhost/user_template?charset=utf8mb4'


class DevConfig(Config):
    """Development configuration."""

    ENV = 'dev'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:@localhost/user_template?charset=utf8mb4'
    SQLALCHEMY_ECHO = False


class LocalConfig(Config):
    ENV = 'local'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:@localhost/user_template?charset=utf8mb4'
    SQLALCHEMY_ECHO = False
