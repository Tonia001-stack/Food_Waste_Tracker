# create_db.py
from app import create_app, db

def create_database():
    app = create_app()
    
    with app.app_context():
        try:
            print("🗄️ Creating database tables...")
            db.create_all()
            print("✅ Database tables created successfully!")
            
            # List all created tables
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            print("📊 Tables created:")
            for table in tables:
                print(f"   - {table}")
                
        except Exception as e:
            print(f"❌ Error creating database: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    create_database()# create_db.py
from app import create_app, db

def create_database():
    app = create_app()
    
    with app.app_context():
        try:
            print("🗄️ Creating database tables...")
            db.create_all()
            print("✅ Database tables created successfully!")
            
            # List all created tables
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            print("📊 Tables created:")
            for table in tables:
                print(f"   - {table}")
                
        except Exception as e:
            print(f"❌ Error creating database: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    create_database()