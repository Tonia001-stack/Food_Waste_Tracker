from app import db
from datetime import datetime

class Donation(db.Model):
    __tablename__ = 'donations'
    
    id = db.Column(db.Integer, primary_key=True)
    food_item_id = db.Column(db.Integer, db.ForeignKey('food_items.id'), nullable=False)
    donor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    claimant_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    quantity = db.Column(db.String(50), nullable=False)  # Changed from db.Float to db.String(50)
    description = db.Column(db.Text)
    pickup_location = db.Column(db.String(200), nullable=False)
    pickup_instructions = db.Column(db.Text)
    
    status = db.Column(db.String(20), default='available')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    claimed_at = db.Column(db.DateTime)
    delivered_at = db.Column(db.DateTime)
    
    # FIXED: Simplified relationships - using backref instead of back_populates
    # The relationships are defined in the User model

    def __repr__(self):
        return f'<Donation {self.id} - {self.status}>'