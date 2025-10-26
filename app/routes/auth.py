"""
Authentication routes for user registration, login, and logout.
Handles user sessions and access control.
"""

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from flask import Blueprint
from app import db
from app.models import User
from app.forms import LoginForm, RegistrationForm

# Create blueprint for auth routes
bp = Blueprint('auth', __name__)

@bp.route('/')
@bp.route('/index')
def index():
    """
    Homepage route.
    Redirects authenticated users to dashboard, shows landing page for others.
    """
    # Check if user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('food.dashboard'))
    
    # Show landing page for non-authenticated users
    return render_template('landing.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    User registration route.
    Handles both form display (GET) and form processing (POST).
    """
    # Redirect if user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('food.dashboard'))
    
    # Create form instance
    form = RegistrationForm()
    
    # Process form submission
    if form.validate_on_submit():
        # Create new user with form data
        user = User(
            username=form.username.data, 
            email=form.email.data,
            user_type=form.user_type.data, 
            location=form.location.data
        )
        user.set_password(form.password.data)
        
        # Save user to database
        db.session.add(user)
        db.session.commit()
        
        # Show success message and redirect to login
        flash('Congratulations, you are now registered! Please log in.')
        return redirect(url_for('auth.login'))
    
    # Show registration form
    return render_template('register.html', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    User login route.
    Handles authentication and session creation.
    """
    # Redirect if user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('food.dashboard'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        # Find user by username
        user = User.query.filter_by(username=form.username.data).first()
        
        # Check if user exists and password is correct
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        
        # Log user in and create session
        login_user(user, remember=form.remember_me.data)
        
        # Redirect to dashboard after successful login
        return redirect(url_for('food.dashboard'))
    
    # Show login form
    return render_template('login.html', form=form)

@bp.route('/logout')
def logout():
    """
    User logout route.
    Ends the user session and redirects to homepage.
    """
    logout_user()
    return redirect(url_for('auth.index'))