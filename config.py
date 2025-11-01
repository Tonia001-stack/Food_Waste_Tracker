"""
========================================
FoodSave Configuration Module
========================================

Configuration settings for the Flask application.
Uses environment variables for security with fallback defaults.

Author: Anthonia Othetheaso
Project: Food Waste Tracker (SDG 2: Zero Hunger)
========================================
"""

import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change-in-production-12345'

    # ==================== Database Configuration ====================

    # Get database URL (Render/Supabase/Railway)
    db_url = os.environ.get("DATABASE_URL") or \
        'sqlite:///' + os.path.join(basedir, 'app.db')

    # Convert URL to psycopg3 format
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql+psycopg://", 1)
    elif db_url.startswith("postgresql://"):
        db_url = db_url.replace("postgresql://", "postgresql+psycopg://", 1)

    SQLALCHEMY_DATABASE_URI = db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'pool_size': 10,
        'max_overflow': 20,
        'pool_timeout': 30,
        'echo': False,
    }

    # ==================== Cookie & Session Security ====================
    SESSION_COOKIE_SECURE = os.environ.get('FLASK_ENV') == 'production'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

    REMEMBER_COOKIE_SECURE = os.environ.get('FLASK_ENV') == 'production'
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SAMESITE = 'Lax'

    REMEMBER_COOKIE_DURATION = timedelta(days=30)
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    # ==================== App-Specific Settings ====================
    WASTE_ALERT_DAYS = 3
    DONATION_RADIUS_KM = 10
    ITEMS_PER_PAGE = 10
    DONATIONS_PER_PAGE = 12

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    UPLOAD_FOLDER = os.path.join(basedir, 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    # ==================== Email Config ====================
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or 'noreply@foodsave.com'

    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    SESSION_COOKIE_SAMESITE = 'Strict'
    PROPAGATE_EXCEPTIONS = False

    @classmethod
    def init_app(cls, app):
        if not os.environ.get('SECRET_KEY'):
            raise ValueError("SECRET_KEY is required in production!")

        if not os.environ.get('DATABASE_URL'):
            raise ValueError("DATABASE_URL is required in production!")

        import logging
        from logging import StreamHandler

        stream_handler = StreamHandler()
        stream_handler.setLevel(logging.INFO)
        app.logger.addHandler(stream_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('🚀 Running in Production Mode')


class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
    SESSION_COOKIE_SECURE = False
    REMEMBER_COOKIE_SECURE = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        **Config.SQLALCHEMY_ENGINE_OPTIONS,
        'echo': False
    }
    TEMPLATES_AUTO_RELOAD = True
    SEND_FILE_MAX_AGE_DEFAULT = 0


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    BCRYPT_LOG_ROUNDS = 4
    MAIL_SUPPRESS_SEND = True
    MAX_CONTENT_LENGTH = None
    SQLALCHEMY_ENGINE_OPTIONS = {
        'echo': False,
        'pool_pre_ping': False,
    }


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config(env=None):
    if env is None:
        env = os.environ.get('FLASK_ENV', 'development')
    config_class = config.get(env, config['default'])
    print(f"🔧 Using configuration: {config_class.__name__}")
    return config_class
