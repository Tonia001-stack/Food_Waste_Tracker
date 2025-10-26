from app import db
from datetime import datetime

class Achievement(db.Model):
    __tablename__ = 'achievements'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    earned_at = db.Column(db.DateTime, default=datetime.utcnow)
    progress = db.Column(db.Integer, default=100)
    target_value = db.Column(db.Integer, default=1)

    # Relationship defined in User model

    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'name': self.name,
            'description': self.description,
            'earned_at': self.earned_at.isoformat() if self.earned_at else None,
            'progress': self.progress,
            'target_value': self.target_value
        }

    def __repr__(self):
        return f'<Achievement {self.name} - {self.user_id}>'

# Achievement definitions
ACHIEVEMENTS = {
    'first_donation': {
        'name': 'First Donation', 
        'description': 'Made your first food donation',
        'type': 'donation',
        'target': 1
    },
    'waste_warrior': {
        'name': 'Waste Warrior', 
        'description': 'Prevented 10+ items from going to waste',
        'type': 'waste_prevention',
        'target': 10
    },
    'community_hero': {
        'name': 'Community Hero', 
        'description': 'Donated 25+ meals to the community',
        'type': 'community',
        'target': 25
    },
    'fresh_keeper': {
        'name': 'Fresh Keeper', 
        'description': 'Consumed 50+ items before expiry',
        'type': 'consumption',
        'target': 50
    }
}

def check_achievements(user, achievement_type, current_count):
    from app.models import Achievement
    
    earned_achievements = []
    
    for achievement_key, achievement_data in ACHIEVEMENTS.items():
        if achievement_data['type'] == achievement_type:
            existing = Achievement.query.filter_by(
                user_id=user.id, 
                name=achievement_data['name']
            ).first()
            
            if not existing and current_count >= achievement_data['target']:
                new_achievement = Achievement(
                    user_id=user.id,
                    type=achievement_data['type'],
                    name=achievement_data['name'],
                    description=achievement_data['description'],
                    progress=100,
                    target_value=achievement_data['target']
                )
                db.session.add(new_achievement)
                earned_achievements.append(new_achievement)
    
    if earned_achievements:
        db.session.commit()
    
    return earned_achievements