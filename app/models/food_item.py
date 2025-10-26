from app import db
from datetime import datetime, date, time, timezone

class FoodItem(db.Model):
    __tablename__ = 'food_items'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.String(50))
    purchase_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    expiry_date = db.Column(db.DateTime, nullable=False)
    current_status = db.Column(db.String(20), default='fresh')
    notes = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # FIXED: Simplified relationship
    donations = db.relationship('Donation', backref='food_item', lazy='dynamic')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.update_status()

    def days_until_expiry(self):
        if isinstance(self.expiry_date, date) and not isinstance(self.expiry_date, datetime):
            expiry_datetime = datetime.combine(self.expiry_date, time.min)
        else:
            expiry_datetime = self.expiry_date
            
        today = datetime.now(timezone.utc).date()
        expiry_date_only = expiry_datetime.date()
        
        return (expiry_date_only - today).days

    def update_status(self):
        days_left = self.days_until_expiry()
        
        if days_left < 0:
            self.current_status = 'expired'
        elif days_left <= 3:
            self.current_status = 'expiring_soon'
        else:
            self.current_status = 'fresh'

    def mark_consumed(self):
        self.current_status = 'consumed'

    def mark_wasted(self):
        self.current_status = 'wasted'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'quantity': self.quantity,
            'purchase_date': self.purchase_date.isoformat() if self.purchase_date else None,
            'expiry_date': self.expiry_date.isoformat() if self.expiry_date else None,
            'status': self.current_status,
            'days_until_expiry': self.days_until_expiry(),
            'notes': self.notes,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f'<FoodItem {self.name} - {self.current_status}>'

# Food categories as constants (simpler than Enum)
FOOD_CATEGORIES = [
    'Fruits', 'Vegetables', 'Dairy', 'Meat', 
    'Grains', 'Beverages', 'Other'
]
    