"""
Application entry point.
Starts the Flask development server and provides shell context.
"""

from app import create_app, db
from app.models import User, FoodItem, Donation

# Create application instance using factory pattern
app = create_app()

@app.shell_context_processor
def make_shell_context():
    """
    Add database and models to Flask shell context.
    This allows easy access to these objects when using 'flask shell'
    
    Returns:
        dict: Context with database and models
    """
    return {
        'db': db,
        'User': User,
        'FoodItem': FoodItem, 
        'Donation': Donation
    }

if __name__ == '__main__':
    """
    Run the application in development mode.
    This block only executes when run directly, not when imported.
    """
    # Start Flask development server
    # debug=True enables auto-reload and detailed error pages
    app.run(debug=True)