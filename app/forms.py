"""
Form definitions using Flask-WTF for form handling and validation.
These forms handle user input with built-in validation and CSRF protection.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models import User
from datetime import date

class LoginForm(FlaskForm):
    """
    Form for user authentication (login).
    Validates username and password credentials.
    """
    
    # Username field - required input
    username = StringField('Username', validators=[DataRequired()])
    
    # Password field - required input, hidden input type
    password = PasswordField('Password', validators=[DataRequired()])
    
    # Remember me checkbox - optional
    remember_me = BooleanField('Remember Me')
    
    # Submit button
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    """
    Form for new user registration.
    Includes validation for unique username and email.
    """
    
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    
    # Password with confirmation field
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', 
        validators=[DataRequired(), EqualTo('password')]  # Must match 'password' field
    )
    
    # User type selection
    user_type = SelectField('User Type', choices=[
        ('individual', 'Individual'),      # Regular user
        ('business', 'Business'),          # Restaurant/store
        ('charity', 'Charity')             # Food bank/charity
    ], validators=[DataRequired()])
    
    location = StringField('Location', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        """
        Custom validator to check if username is already taken.
        WTForms automatically calls methods starting with 'validate_'
        
        Args:
            username: username field from form
            
        Raises:
            ValidationError: If username already exists
        """
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        """
        Custom validator to check if email is already registered.
        
        Args:
            email: email field from form
            
        Raises:
            ValidationError: If email already exists
        """
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class AddFoodForm(FlaskForm):
    """
    Form for adding new food items to inventory.
    Tracks food details including expiry dates.
    """
    
    name = StringField('Food Item Name', validators=[DataRequired()])
    
    # Food category selection
    category = SelectField('Category', choices=[
        ('FRUITS', 'Fruits'),
        ('VEGETABLES', 'Vegetables'), 
        ('DAIRY', 'Dairy'),
        ('MEAT', 'Meat'),
        ('GRAINS', 'Grains'),
        ('BEVERAGES', 'Beverages'),
        ('OTHER', 'Other')
    ], validators=[DataRequired()])
    
    # Flexible quantity field (grams, pieces, liters, etc.)
    quantity = StringField('Quantity (e.g., 500g, 2 pieces)', validators=[DataRequired()])
    
    # Date fields with today as default for purchase date
    purchase_date = DateField('Purchase Date', default=date.today)
    expiry_date = DateField('Expiry Date', validators=[DataRequired()])
    
    # Optional notes field
    notes = TextAreaField('Additional Notes')
    
    submit = SubmitField('Add Food Item')