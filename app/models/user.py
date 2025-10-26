from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager
from datetime import datetime, timezone

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128))
    user_type = db.Column(db.String(20), default='individual')
    location = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    # FIXED: Use string-based relationships to avoid circular imports
    food_items = db.relationship('FoodItem', backref='owner', lazy='dynamic')
    donations_made = db.relationship('Donation', 
                                   foreign_keys='Donation.donor_id',
                                   backref='donor',
                                   lazy='dynamic')
    donations_claimed = db.relationship('Donation', 
                                      foreign_keys='Donation.claimant_id', 
                                      backref='claimant',
                                      lazy='dynamic')
    achievements = db.relationship('Achievement', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

@login_manager.user_loader
def load_user(id):
    return db.session.get(User, int(id))