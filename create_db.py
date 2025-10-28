"""
Database Creation and Migration Script

This script creates all database tables and can be used for initial setup
or testing. For production, use Flask-Migrate instead.

Usage:
    python create_db.py
"""

from app import create_app, db
from app.models import User, FoodItem, Donation
import os


def create_database():
    """
    Create all database tables defined in models.
    
    This function:
    1. Creates Flask app instance
    2. Creates all tables from SQLAlchemy models
    3. Displays confirmation and table list
    """
    app = create_app()
    
    with app.app_context():
        try:
            # Display database being used
            db_uri = app.config['SQLALCHEMY_DATABASE_URI']
            if 'sqlite' in db_uri:
                print("🗄️  Using SQLite database (local)")
            elif 'postgresql' in db_uri or 'postgres' in db_uri:
                # Hide password in display
                safe_uri = db_uri.split('@')[1] if '@' in db_uri else db_uri
                print(f"🐘 Using PostgreSQL database: {safe_uri}")
            
            print("\n📦 Creating database tables...")
            
            # Create all tables
            db.create_all()
            
            print("✅ Database tables created successfully!\n")
            
            # List all created tables
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            
            print("📊 Tables created:")
            for table in tables:
                # Get column count
                columns = inspector.get_columns(table)
                print(f"   ✓ {table} ({len(columns)} columns)")
            
            print(f"\n🎉 Total: {len(tables)} tables ready!")
            
            # Verify models are registered
            print("\n🔍 Registered Models:")
            print(f"   - User: {User.__tablename__}")
            print(f"   - FoodItem: {FoodItem.__tablename__}")
            print(f"   - Donation: {Donation.__tablename__}")
            
        except Exception as e:
            print(f"\n❌ Error creating database: {e}")
            print("\n💡 Troubleshooting tips:")
            print("   1. Check your DATABASE_URL in .env")
            print("   2. Verify database credentials")
            print("   3. Ensure psycopg2-binary is installed")
            print("   4. Check internet connection (for remote DB)")
            
            import traceback
            print("\n🔴 Full error trace:")
            traceback.print_exc()


def drop_and_recreate():
    """
    Drop all tables and recreate them (DESTRUCTIVE).
    
    WARNING: This will delete ALL data in the database!
    Only use in development.
    """
    app = create_app()
    
    with app.app_context():
        if os.environ.get('FLASK_ENV') == 'production':
            print("❌ Cannot drop tables in production!")
            return
        
        confirm = input("⚠️  This will DELETE ALL DATA. Type 'yes' to confirm: ")
        if confirm.lower() != 'yes':
            print("❌ Operation cancelled.")
            return
        
        try:
            print("\n🗑️  Dropping all tables...")
            db.drop_all()
            print("✅ Tables dropped")
            
            print("\n📦 Recreating tables...")
            db.create_all()
            print("✅ Tables recreated\n")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()


if __name__ == '__main__':
    import sys
    
    print("\n" + "="*60)
    print("🍎 FoodSave Database Setup")
    print("="*60)
    
    # Check if .env exists
    if not os.path.exists('.env'):
        print("\n⚠️  WARNING: .env file not found!")
        print("Create a .env file with your DATABASE_URL")
        print("\nExample:")
        print("DATABASE_URL=postgresql://user:pass@host:5432/dbname")
        print("="*60 + "\n")
    
    # Check for command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == '--reset':
        drop_and_recreate()
    else:
        create_database()
    
    print("\n" + "="*60)
    print("✨ Done!")
    print("="*60 + "\n")