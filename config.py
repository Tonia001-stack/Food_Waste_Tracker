"""
Configuration settings for the Flask application.
Uses environment variables for security with fallback defaults.
"""

import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the base directory of the application
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """
    Base configuration class with common settings for all environments.
    
    Attributes:
        SECRET_KEY (str): Secret key for securing sessions and tokens
        SQLALCHEMY_DATABASE_URI (str): Database connection string
        SQLALCHEMY_TRACK_MODIFICATIONS (bool): Disable Flask-SQLAlchemy event system
        WASTE_ALERT_DAYS (int): Days before expiry to alert users
        DONATION_RADIUS_KM (int): Radius for donation matching in kilometers
    """
    
    # Secret key for securing sessions and tokens
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-change-in-production'
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    
    # Fix for PostgreSQL URL in production (common deployment issue)
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)
    
    # Disable track modifications to save memory and prevent warnings
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Security settings for production
    SESSION_COOKIE_SECURE = os.environ.get('FLASK_ENV') == 'production'  # HTTPS only in production
    SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript access to cookies
    REMEMBER_COOKIE_SECURE = os.environ.get('FLASK_ENV') == 'production'
    REMEMBER_COOKIE_HTTPONLY = True
    
    # Food waste application specific settings
    WASTE_ALERT_DAYS = 3  # Alert when food is 3 days from expiry
    DONATION_RADIUS_KM = 10  # Default radius for donation matching


class ProductionConfig(Config):
    """
    Production environment configuration.
    
    Security-focused settings for live deployment.
    """
    DEBUG = False
    TESTING = False
    
    # Additional production security
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True


class DevelopmentConfig(Config):
    """
    Development environment configuration.
    
    Debug-friendly settings for local development.
    """
    DEBUG = True
    DEVELOPMENT = True
    # Development can use HTTP
    SESSION_COOKIE_SECURE = False
    REMEMBER_COOKIE_SECURE = False


class TestingConfig(Config):
    """
    Testing environment configuration.
    
    Isolated settings for automated testing.
    """
    TESTING = True
    DEBUG = True
    # Use in-memory SQLite for fast, isolated tests
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    # Disable CSRF protection for easier testing
    WTF_CSRF_ENABLED = False