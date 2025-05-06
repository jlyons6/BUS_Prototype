from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

# Initialize extensions
db = SQLAlchemy()
login = LoginManager()
login.login_view = 'main.login'
login.login_message = 'Please log in to access this page.'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions
    db.init_app(app)
    login.init_app(app)

    # Register blueprints
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    # Register CLI commands
    from app.debug_utils import populate_db, reset_db
    @app.cli.command("init-db")
    def init_db_command():
        """Initialize the database with test data."""
        populate_db()
        print("Database initialized with test data.")

    @app.cli.command("reset-db")
    def reset_db_command():
        """Reset the database."""
        reset_db()
        print("Database reset complete.")

    return app

from app import models 