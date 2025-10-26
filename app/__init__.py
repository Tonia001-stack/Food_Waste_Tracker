from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__)
    
    # FORCE PRODUCTION CONFIG - REMOVE ENVIRONMENT DETECTION
    from config import ProductionConfig
    app.config.from_object(ProductionConfig)
    print("🚀 FORCING PRODUCTION CONFIGURATION")
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    
    # Register blueprints
    from app.routes import main, auth, food, donations, analytics
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(food.bp)
    app.register_blueprint(donations.bp)
    app.register_blueprint(analytics.bp)
    
    return app

# Import models here to avoid circular imports
from app.models import User, FoodItem, Donation, Achievement
