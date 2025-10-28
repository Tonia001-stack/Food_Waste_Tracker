"""
========================================
FoodSave Configuration Module
========================================

Configuration settings for the Flask application.
Uses environment variables for security with fallback defaults.

Author: Anthonia Othetheaso
Project: Food Waste Tracker (SDG 2: Zero Hunger)

Environments:
    - Development: Local development with debug mode
    - Production: Live deployment with enhanced security
    - Testing: Automated testing with in-memory database
========================================
"""

import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
# This must be done before accessing any environment variables
load_dotenv()

# Get the base directory of the application
# Used for constructing absolute file paths
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """
    Base configuration class with common settings for all environments.
    
    This class contains default settings that are inherited by all other
    configuration classes. Environment-specific settings should be defined
    in the respective child classes (DevelopmentConfig, ProductionConfig, etc.)
    
    Attributes:
        SECRET_KEY (str): Secret key for securing sessions, cookies, and CSRF tokens
        SQLALCHEMY_DATABASE_URI (str): Database connection string (SQLite/PostgreSQL)
        SQLALCHEMY_TRACK_MODIFICATIONS (bool): Disable Flask-SQLAlchemy event system
        SQLALCHEMY_ENGINE_OPTIONS (dict): Database engine configuration options
        SESSION_COOKIE_SECURE (bool): Require HTTPS for session cookies
        SESSION_COOKIE_HTTPONLY (bool): Prevent JavaScript access to session cookies
        SESSION_COOKIE_SAMESITE (str): CSRF protection for cookies
        REMEMBER_COOKIE_SECURE (bool): Require HTTPS for remember-me cookies
        REMEMBER_COOKIE_HTTPONLY (bool): Prevent JavaScript access to remember-me cookies
        REMEMBER_COOKIE_DURATION (timedelta): Duration for remember-me functionality
        PERMANENT_SESSION_LIFETIME (timedelta): Session expiration time
        WASTE_ALERT_DAYS (int): Days before expiry to alert users about expiring food
        DONATION_RADIUS_KM (int): Default radius for donation matching in kilometers
        ITEMS_PER_PAGE (int): Number of items to display per page in lists
        DONATIONS_PER_PAGE (int): Number of donations to display per page
        MAX_CONTENT_LENGTH (int): Maximum file upload size in bytes
    """
    
    # ==================== Security Configuration ====================
    
    # Secret key for securing sessions, cookies, and CSRF tokens
    # CRITICAL: Must be set via environment variable in production
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change-in-production-12345'
    
    # Warn if using default secret key
    if SECRET_KEY == 'dev-key-please-change-in-production-12345':
        import warnings
        warnings.warn(
            "WARNING: Using default SECRET_KEY. Set SECRET_KEY environment variable for security!",
            RuntimeWarning
        )
    
    # ==================== Database Configuration ====================
    
    # Database connection string
    # Supports both SQLite (development) and PostgreSQL (production/Supabase)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    
    # Fix for PostgreSQL URL format in production deployments
    # Some platforms (Heroku, older Render) use deprecated 'postgres://' prefix
    # Supabase and modern PostgreSQL use 'postgresql://'
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace(
            "postgres://", "postgresql://", 1
        )
    
    # Disable modification tracking to save memory and prevent unnecessary overhead
    # Flask-SQLAlchemy's event system is not needed for this application
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Database connection pool settings for better performance and reliability
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,      # Verify connections before using them
        'pool_recycle': 300,        # Recycle connections after 5 minutes
        'pool_size': 10,            # Number of connections to maintain
        'max_overflow': 20,         # Maximum overflow connections
        'pool_timeout': 30,         # Timeout for getting connection from pool
        'echo': False,              # Set to True to log all SQL statements
    }
    
    # ==================== Session & Cookie Security ====================
    
    # Enable secure cookies only in production (requires HTTPS)
    SESSION_COOKIE_SECURE = os.environ.get('FLASK_ENV') == 'production'
    
    # Prevent JavaScript access to session cookies (XSS protection)
    SESSION_COOKIE_HTTPONLY = True
    
    # CSRF protection for cookies - prevents cross-site request forgery
    SESSION_COOKIE_SAMESITE = 'Lax'  # 'Strict' for maximum security, 'Lax' for usability
    
    # Apply same security settings to remember-me cookies
    REMEMBER_COOKIE_SECURE = os.environ.get('FLASK_ENV') == 'production'
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SAMESITE = 'Lax'
    
    # Remember me duration - how long "remember me" stays active
    REMEMBER_COOKIE_DURATION = timedelta(days=30)
    
    # Session lifetime - sessions expire after 7 days of inactivity
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # ==================== Application-Specific Settings ====================
    
    # Food waste tracking settings
    WASTE_ALERT_DAYS = 3  # Alert when food is 3 days from expiry
    
    # Donation system settings
    DONATION_RADIUS_KM = 10  # Default radius for donation matching
    
    # Pagination settings
    ITEMS_PER_PAGE = 10         # Number of food items per page
    DONATIONS_PER_PAGE = 12     # Number of donations per page
    
    # File upload settings (for future features like food photos)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = os.path.join(basedir, 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    
    # ==================== Email Configuration (Optional) ====================
    
    # Email settings for notifications (configure if you want email alerts)
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or 'noreply@foodsave.com'
    
    # ==================== Logging Configuration ====================
    
    # Log level - can be DEBUG, INFO, WARNING, ERROR, CRITICAL
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    
    # ==================== Feature Flags ====================
    
    # Enable/disable features via environment variables
    ENABLE_EMAIL_NOTIFICATIONS = os.environ.get('ENABLE_EMAIL_NOTIFICATIONS', 'false').lower() == 'true'
    ENABLE_SMS_NOTIFICATIONS = os.environ.get('ENABLE_SMS_NOTIFICATIONS', 'false').lower() == 'true'


class ProductionConfig(Config):
    """
    Production environment configuration.
    
    Security-focused settings for live deployment on platforms like
    Render, Railway, Heroku, or custom servers with Supabase database.
    
    Key differences from base Config:
    - Debug mode disabled for security
    - Testing disabled
    - Secure cookies enforced (requires HTTPS)
    - Stricter error handling
    - Production-optimized settings
    """
    
    # Disable debug mode in production for security
    DEBUG = False
    TESTING = False
    
    # Force secure cookies in production (requires HTTPS)
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    
    # Use stricter SameSite policy in production
    SESSION_COOKIE_SAMESITE = 'Strict'
    
    # Don't propagate exceptions to user in production
    PROPAGATE_EXCEPTIONS = False
    
    # Ensure database URL is set in production
    @classmethod
    def init_app(cls, app):
        """Initialize production-specific settings."""
        # Validate critical settings
        if not os.environ.get('SECRET_KEY'):
            raise ValueError("SECRET_KEY environment variable must be set in production!")
        
        if not os.environ.get('DATABASE_URL'):
            raise ValueError("DATABASE_URL environment variable must be set in production!")
        
        # Log to stdout in production (for cloud platforms)
        import logging
        from logging import StreamHandler
        
        stream_handler = StreamHandler()
        stream_handler.setLevel(logging.INFO)
        app.logger.addHandler(stream_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('FoodSave production startup')


class DevelopmentConfig(Config):
    """
    Development environment configuration.
    
    Debug-friendly settings for local development with helpful
    error messages and automatic reloading.
    
    Key differences from base Config:
    - Debug mode enabled for detailed error messages
    - Less strict cookie security (HTTP allowed)
    - SQL query logging available
    - Template auto-reload enabled
    - Uses SQLite by default (easier for local dev)
    """
    
    # Enable debug mode for detailed error messages and auto-reload
    DEBUG = True
    DEVELOPMENT = True
    
    # Allow cookies over HTTP in development (no HTTPS required)
    SESSION_COOKIE_SECURE = False
    REMEMBER_COOKIE_SECURE = False
    
    # Enable SQL query logging (useful for debugging)
    # Set to True to see all SQL queries in console
    SQLALCHEMY_ENGINE_OPTIONS = {
        **Config.SQLALCHEMY_ENGINE_OPTIONS,
        'echo': False  # Change to True to log SQL queries
    }
    
    # Reload templates automatically without restarting server
    TEMPLATES_AUTO_RELOAD = True
    
    # Show detailed error pages
    SEND_FILE_MAX_AGE_DEFAULT = 0  # Disable caching for development


class TestingConfig(Config):
    """
    Testing environment configuration.
    
    Isolated settings for automated testing with pytest.
    Uses in-memory database for fast, independent tests.
    
    Key differences from base Config:
    - Testing mode enabled
    - In-memory SQLite database for speed
    - CSRF protection disabled for easier testing
    - Faster password hashing for quicker tests
    - Email sending disabled
    """
    
    # Enable testing mode
    TESTING = True
    DEBUG = True
    
    # Use in-memory SQLite for fast, isolated tests
    # Each test run gets a fresh database that's destroyed after tests
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    
    # Disable CSRF protection for easier form testing
    # Note: In real tests, you should test CSRF protection separately
    WTF_CSRF_ENABLED = False
    
    # Faster password hashing for tests (reduces test execution time)
    # WARNING: Only use this in testing, never in production!
    BCRYPT_LOG_ROUNDS = 4  # Default is 12, lower is faster but less secure
    
    # Disable email sending during tests
    MAIL_SUPPRESS_SEND = True
    
    # Disable file size limits for testing
    MAX_CONTENT_LENGTH = None
    
    # Use synchronous mode for predictable test behavior
    SQLALCHEMY_ENGINE_OPTIONS = {
        'echo': False,
        'pool_pre_ping': False,
    }


# ==================== Configuration Dictionary ====================

# Dictionary to easily select configuration based on environment
# Usage: config_name = os.environ.get('FLASK_ENV', 'development')
#        app.config.from_object(config[config_name])
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config(env=None):
    """
    Get the appropriate configuration class based on environment.
    
    Args:
        env (str, optional): Environment name ('development', 'production', 'testing')
                           If None, uses FLASK_ENV environment variable
    
    Returns:
        Config: Configuration class for the specified environment
    
    Example:
        >>> from config import get_config
        >>> config = get_config('production')
        >>> app.config.from_object(config)
    """
    if env is None:
        env = os.environ.get('FLASK_ENV', 'development')
    
    config_class = config.get(env, config['default'])
    
    # Print configuration being used (helpful for debugging)
    print(f"🔧 Using configuration: {config_class.__name__}")
    
    return config_class