from app import create_app, db
from app.debug_utils import populate_db

app = create_app()

with app.app_context():
    # Create all tables
    db.create_all()
    print("Database tables created.")
    
    # Populate with test data
    populate_db()
    print("Database initialized with test data.") 