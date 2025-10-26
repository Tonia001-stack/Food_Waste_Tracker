"""
Donation routes for food donation marketplace.
Handles creating, viewing, and claiming food donations.
"""

from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from flask import Blueprint
from app import db
from app.models import Donation, FoodItem, User
from datetime import datetime, timezone

# Create blueprint for donation routes
bp = Blueprint('donations', __name__)

@bp.route('/donations')
@login_required
def list_donations():
    """
    Display all available food donations.
    Shows donations that haven't been claimed yet.
    """
    # Get page number from URL parameters (for pagination)
    page = request.args.get('page', 1, type=int)
    
    # FIXED: Use correct relationship names - remove donor_user and claimant_user
    donations = Donation.query.filter_by(status='available')\
        .options(db.joinedload(Donation.food_item))\
        .options(db.joinedload(Donation.donor))\
        .paginate(page=page, per_page=10, error_out=False)
    
    return render_template('list.html', donations=donations)

@bp.route('/my_donations')
@login_required
def my_donations():
    """
    Show donations created by the current user.
    Includes all statuses (available, claimed, delivered).
    """
    # FIXED: Use correct relationship names
    donations = Donation.query.filter_by(donor_id=current_user.id)\
        .options(db.joinedload(Donation.food_item))\
        .options(db.joinedload(Donation.claimant))\
        .all()
    
    return render_template('my_donations.html', donations=donations)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_donation():
    """
    Create a new food donation from user's inventory.
    Converts a food item into a donation listing.
    """
    # Get user's food items that are suitable for donation
    food_items = FoodItem.query.filter(
        FoodItem.user_id == current_user.id,
        FoodItem.current_status.in_(['fresh', 'expiring_soon'])
    ).all()
    
    if request.method == 'POST':
        food_item_id = request.form.get('food_item_id')
        quantity = request.form.get('quantity')
        description = request.form.get('description')
        pickup_location = request.form.get('pickup_location')
        
        if not food_item_id:
            flash('Please select a food item to donate.', 'error')
            return render_template('create.html', food_items=food_items)
        
        # Get the food item being donated
        food_item = FoodItem.query.get(food_item_id)
        
        if not food_item:
            flash('Food item not found.', 'error')
            return render_template('create.html', food_items=food_items)
        
        # Create donation record
        donation = Donation(
            food_item_id=food_item_id,
            donor_id=current_user.id,
            quantity=quantity or food_item.quantity,
            description=description,
            pickup_location=pickup_location,
            status='available'
        )
        
        # Update food item status to 'donated'
        food_item.current_status = 'donated'
        
        # Save both changes to database
        db.session.add(donation)
        db.session.commit()
        
        # Check for first donation achievement
        user_donation_count = Donation.query.filter_by(donor_id=current_user.id).count()
        if user_donation_count == 1:
            check_achievements(current_user.id, 'first_donation')
        
        flash('Donation created successfully! Your food item has been marked as donated.', 'success')
        return redirect(url_for('donations.my_donations'))
    
    return render_template('create.html', food_items=food_items)

@bp.route('/claim/<int:donation_id>', methods=['POST'])
@login_required
def claim_donation(donation_id):
    """
    Claim an available food donation.
    Changes donation status from 'available' to 'claimed'.
    """
    # FIXED: Use correct relationship names
    donation = Donation.query.filter_by(id=donation_id)\
        .options(db.joinedload(Donation.food_item))\
        .options(db.joinedload(Donation.donor))\
        .first_or_404()
    
    # Check if donation is still available
    if donation.status != 'available':
        flash('This donation is no longer available.', 'error')
        return redirect(url_for('donations.list_donations'))
    
    # Check if user is trying to claim their own donation
    if donation.donor_id == current_user.id:
        flash('You cannot claim your own donation.', 'error')
        return redirect(url_for('donations.list_donations'))
    
    # Update donation status and record claimant
    donation.status = 'claimed'
    donation.claimant_id = current_user.id
    donation.claimed_at = datetime.now(timezone.utc)
    
    db.session.commit()
    
    flash('Donation claimed successfully! You can now contact the donor.', 'success')
    # Redirect to contact page instead of claims list
    return redirect(url_for('donations.contact_donor', donation_id=donation.id))

@bp.route('/contact/<int:donation_id>')
@login_required
def contact_donor(donation_id):
    """
    Show donor contact information for a claimed donation.
    """
    # FIXED: Use correct relationship names
    donation = Donation.query.filter_by(id=donation_id)\
        .options(db.joinedload(Donation.donor))\
        .options(db.joinedload(Donation.food_item))\
        .first_or_404()
    
    # Security: only the claimant or donor can see contact info
    if donation.claimant_id != current_user.id and donation.donor_id != current_user.id:
        flash('You are not authorized to view this information.', 'error')
        return redirect(url_for('donations.list_donations'))
    
    return render_template('contact_donor.html', donation=donation)

@bp.route('/send_message/<int:donation_id>', methods=['POST'])
@login_required
def send_message(donation_id):
    """
    Send a message to the donor/claimant.
    This is a simplified version that just shows a success message.
    """
    donation = Donation.query.get_or_404(donation_id)
    message = request.form.get('message')
    
    if not message:
        flash('Please enter a message.', 'error')
        return redirect(url_for('donations.contact_donor', donation_id=donation_id))
    
    # Security check
    if current_user.id not in [donation.donor_id, donation.claimant_id]:
        flash('You are not authorized to send messages for this donation.', 'error')
        return redirect(url_for('donations.list_donations'))
    
    # Determine who is the recipient
    if current_user.id == donation.claimant_id:
        # Claimant is sending to donor
        recipient_email = donation.donor.email
        recipient_name = donation.donor.username
        flash(f'Message prepared for {recipient_name}! You can now email them at: {recipient_email}', 'success')
    else:
        # Donor is sending to claimant
        recipient_email = donation.claimant.email
        recipient_name = donation.claimant.username
        flash(f'Message prepared for {recipient_name}! You can now email them at: {recipient_email}', 'success')
    
    return redirect(url_for('donations.contact_donor', donation_id=donation_id))

@bp.route('/my_claims')
@login_required
def my_claims():
    """
    Show donations claimed by the current user.
    """
    # FIXED: Use correct relationship names
    claims = Donation.query.filter_by(claimant_id=current_user.id)\
        .options(db.joinedload(Donation.food_item))\
        .options(db.joinedload(Donation.donor))\
        .all()
    
    return render_template('my_claims.html', claims=claims)

@bp.route('/complete/<int:donation_id>', methods=['POST'])
@login_required
def complete_donation(donation_id):
    """
    Mark a donation as delivered/completed.
    Only the original donor can complete a donation.
    """
    donation = Donation.query.get_or_404(donation_id)
    
    # Security check: only the donor can complete the donation
    if donation.donor_id != current_user.id:
        flash('You are not authorized to complete this donation.', 'error')
        return redirect(url_for('donations.my_donations'))
    
    # Update status to completed
    donation.status = 'completed'
    donation.completed_at = datetime.now(timezone.utc)
    db.session.commit()
    
    flash('Donation marked as completed!', 'success')
    return redirect(url_for('donations.my_donations'))

@bp.route('/cancel/<int:donation_id>', methods=['POST'])
@login_required
def cancel_donation(donation_id):
    """
    Cancel a donation (only available or claimed donations can be cancelled).
    """
    donation = Donation.query.get_or_404(donation_id)
    
    # Security check: only the donor can cancel the donation
    if donation.donor_id != current_user.id:
        flash('You are not authorized to cancel this donation.', 'error')
        return redirect(url_for('donations.my_donations'))
    
    # Only allow cancellation of available or claimed donations
    if donation.status not in ['available', 'claimed']:
        flash('This donation cannot be cancelled.', 'error')
        return redirect(url_for('donations.my_donations'))
    
    # Reset donation status and clear claimant info
    donation.status = 'cancelled'
    donation.claimant_id = None
    donation.claimed_at = None
    
    # Reset the food item status back to its original state
    food_item = FoodItem.query.get(donation.food_item_id)
    if food_item:
        food_item.current_status = 'fresh'  # Or determine based on expiry date
    
    db.session.commit()
    
    flash('Donation cancelled successfully.', 'success')
    return redirect(url_for('donations.my_donations'))

@bp.route('/api/nearby')
@login_required
def api_nearby_donations():
    """
    API endpoint for nearby donations (simplified version).
    """
    # FIXED: Use correct relationship names
    donations = Donation.query.filter_by(status='available')\
        .options(db.joinedload(Donation.food_item))\
        .options(db.joinedload(Donation.donor))\
        .limit(20)\
        .all()
    
    # Convert to JSON-friendly format
    donations_data = []
    for donation in donations:
        donations_data.append({
            'id': donation.id,
            'food_name': donation.food_item.name,
            'quantity': donation.quantity,
            'description': donation.description,
            'pickup_location': donation.pickup_location,
            'donor': donation.donor.username,
            'created_at': donation.created_at.isoformat() if donation.created_at else None
        })
    
    return jsonify(donations_data)

def check_achievements(user_id, achievement_type):
    """
    Check and award achievements to users.
    """
    from app.models.achievement import Achievement, ACHIEVEMENTS
    
    # Check if achievement type exists
    if achievement_type not in ACHIEVEMENTS:
        return False
    
    # Check if user already has this achievement
    existing = Achievement.query.filter_by(
        user_id=user_id, 
        type=achievement_type
    ).first()
    
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
    