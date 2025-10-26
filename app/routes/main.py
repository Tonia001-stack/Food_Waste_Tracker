"""
Analytics routes for food waste tracking and reporting.
Provides insights into user's food consumption and waste patterns.
"""

from flask import render_template, jsonify
from flask_login import login_required, current_user
from flask import Blueprint
from app.models import FoodItem, Donation
from datetime import datetime, timedelta
from sqlalchemy import func

# Create blueprint for analytics routes
bp = Blueprint('analytics', __name__)

@bp.route('/dashboard')
@login_required
def dashboard():
    """
    Display analytics dashboard with food waste statistics and insights.
    """
    # Get basic statistics
    stats = get_user_stats(current_user.id)
    
    # Calculate environmental impact
    environmental_impact = calculate_environmental_impact(current_user.id)
    
    # Render the template with data
    return render_template('analytics_dashboard.html', 
                         stats=stats, 
                         environmental_impact=environmental_impact)

def get_user_stats(user_id):
    """
    Calculate comprehensive statistics for a user's food inventory.
    """
    # Get all user's food items
    user_items = FoodItem.query.filter_by(user_id=user_id).all()
    
    # Initialize counts
    fresh_count = 0
    expiring_soon_count = 0
    expired_count = 0
    consumed_count = 0
    wasted_count = 0
    donated_count = 0
    
    # Count by status
    for item in user_items:
        if item.current_status == 'fresh':
            fresh_count += 1
        elif item.current_status == 'expiring_soon':
            expiring_soon_count += 1
        elif item.current_status == 'expired':
            expired_count += 1
        elif item.current_status == 'consumed':
            consumed_count += 1
        elif item.current_status == 'wasted':
            wasted_count += 1
        elif item.current_status == 'donated':
            donated_count += 1
    
    # Calculate total items
    total_items = len(user_items)
    
    # Calculate waste percentage (avoid division by zero)
    if total_items > 0:
        waste_percentage = round((wasted_count / total_items) * 100, 1)
    else:
        waste_percentage = 0
    
    return {
        'total_items': total_items,
        'fresh_count': fresh_count,
        'expiring_soon_count': expiring_soon_count,
        'expired_count': expired_count,
        'consumed_count': consumed_count,
        'wasted_count': wasted_count,
        'donated_count': donated_count,
        'waste_percentage': waste_percentage
    }

def calculate_environmental_impact(user_id):
    """
    Calculate environmental impact based on wasted food items.
    """
    wasted_count = FoodItem.query.filter_by(
        user_id=user_id, 
        current_status='wasted'
    ).count()
    
    # Environmental impact calculations
    co2_saved = round(wasted_count * 2.5, 1)  # kg CO2
    water_saved = wasted_count * 1000  # liters
    meals_saved = wasted_count * 3  # potential meals
    
    return {
        'co2_saved': co2_saved,
        'water_saved': water_saved,
        'meals_saved': meals_saved
    }

@bp.route('/api/stats')
@login_required
def api_stats():
    """
    API endpoint for getting user statistics in JSON format.
    """
    stats = get_user_stats(current_user.id)
    return jsonify(stats)

@bp.route('/api/environmental-impact')
@login_required
def api_environmental_impact():
    """
    API endpoint for environmental impact data.
    """
    impact = calculate_environmental_impact(current_user.id)
    return jsonify(impact)


                         