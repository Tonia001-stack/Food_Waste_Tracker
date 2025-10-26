"""
Food tracking routes for managing food inventory.
Handles adding, viewing, and updating food items.
"""

from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from flask import Blueprint
from app import db
from app.models import FoodItem
from app.forms import AddFoodForm
from app.utils.food_calculations import FoodWasteCalculator
from datetime import datetime

# Create blueprint for food-related routes
bp = Blueprint('food', __name__)

@bp.route('/inventory')
@login_required  
def dashboard():
    """
    Food inventory showing user's food items.
    """
    # Get user's food items
    food_items = FoodItem.query.filter_by(user_id=current_user.id).all()
    
    # Update status for all items
    for item in food_items:
        item.update_status()
    
    # Calculate stats
    stats = {
        'total_items': len(food_items),
        'expiring_soon_count': len([item for item in food_items if item.current_status == 'expiring_soon']),
        'expired_count': len([item for item in food_items if item.current_status == 'expired']),
        'consumed_count': len([item for item in food_items if item.current_status == 'consumed']),
        'wasted_count': len([item for item in food_items if item.current_status == 'wasted']),
        'food_items': food_items
    }
    
    # Get items expiring soon for alerts
    expiring_soon = [item for item in food_items if item.current_status == 'expiring_soon']
    
    # Use the new food template instead of dashboard.html
    return render_template('food_simple.html', stats=stats, expiring_soon=expiring_soon)

@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_food():
    """
    Add new food item to inventory.
    Handles both form display (GET) and form processing (POST).
    """
    # Create form instance
    form = AddFoodForm()
    
    # Process form submission
    if form.validate_on_submit():
        # Create new FoodItem with form data
        food_item = FoodItem(
            name=form.name.data,
            category=form.category.data,
            quantity=form.quantity.data,
            purchase_date=form.purchase_date.data or datetime.utcnow(),
            expiry_date=form.expiry_date.data,
            notes=form.notes.data,
            user_id=current_user.id
        )
        
        # Update status based on expiry date
        food_item.update_status()
        
        # Save to database
        db.session.add(food_item)
        db.session.commit()
        
        # Show success message
        flash('Food item added successfully!')
        
        # Redirect to food inventory
        return redirect(url_for('food.dashboard'))
    
    # Show add food form
    return render_template('add_food.html', form=form)

@bp.route('/update_status/<int:item_id>', methods=['POST'])
@login_required
def update_status(item_id):
    """
    API endpoint to update food item status (consumed/wasted).
    Called via JavaScript/AJAX from the frontend.
    """
    # Get the food item from database
    food_item = FoodItem.query.get_or_404(item_id)
    
    # Security check: ensure user owns this item
    if food_item.user_id != current_user.id:
        flash('You cannot modify this item.')
        return redirect(url_for('food.dashboard'))
    
    # Get new status from JSON request
    new_status = request.json.get('status')
    
    # Validate status value
    if new_status in ['consumed', 'wasted']:
        # Update status
        food_item.current_status = new_status
        db.session.commit()
        
        # Return JSON response for AJAX call
        return jsonify({'success': True})
    
    # Return error if status is invalid
    return jsonify({'success': False}), 400

@bp.route('/api/food_items')
@login_required
def api_food_items():
    """
    API endpoint to get user's food items in JSON format.
    """
    # Get all food items for current user
    food_items = FoodItem.query.filter_by(user_id=current_user.id).all()
    
    # Convert to list of dictionaries for JSON response
    items_data = [item.to_dict() for item in food_items]
    
    return jsonify(items_data)

from app.models.achievement import Achievement, ACHIEVEMENTS

def check_achievements(user_id, achievement_type):
    # Check if user already has this achievement
    existing = Achievement.query.filter_by(user_id=user_id, type=achievement_type).first()
    if not existing:
        achievement_data = ACHIEVEMENTS[achievement_type]
        achievement = Achievement(
            user_id=user_id,
            type=achievement_type,
            name=achievement_data['name'],
            description=achievement_data['description']
        )
        db.session.add(achievement)
        db.session.commit()
        return True
    return False