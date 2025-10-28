from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate  # ← ADD THIS IMPORT
import os

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
migrate = Migrate()  # ← ADD THIS LINE

def create_app():
    app = Flask(__name__)
    
    # FORCE PRODUCTION CONFIG
    from config import ProductionConfig
    app.config.from_object(ProductionConfig)
    print("🚀 FORCING PRODUCTION CONFIGURATION")
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)  # ← ADD THIS LINE
    
    # Register blueprints
    from app.routes import main, auth, food, donations
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(food.bp)
    app.register_blueprint(donations.bp)
    
    return app

# Import models here to avoid circular imports
from app.models import User, FoodItem, Donation, Achievement
