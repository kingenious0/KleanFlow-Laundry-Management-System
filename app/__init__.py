"""
Application Factory for KleanFlow Laundry Management System.
"""

import os
from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from app.config import Config, config_by_name
from app.extensions import db, migrate, login_manager


def create_app(config_name=None):
    """
    Flask Application Factory.
    Initializes configuration, extensions, blueprints, error handlers, and login user loader.
    """
    app = Flask(__name__)

    # Determine configuration class
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    app_config = config_by_name.get(config_name, Config)
    app.config.from_object(app_config)

    # Automatic Database Connection Health Check & Fallback
    db_uri = app.config.get('SQLALCHEMY_DATABASE_URI', '')
    if db_uri.startswith('mysql'):
        try:
            # Quick connectivity test
            test_engine = create_engine(db_uri, connect_args={'connect_timeout': 3})
            with test_engine.connect() as conn:
                pass
            test_engine.dispose()
        except OperationalError as e:
            # Fallback to local SQLite instance if MySQL connection/auth fails
            sqlite_db_path = os.path.abspath(os.path.join(app.root_path, '..', 'instance', 'kleanflow.db'))
            app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{sqlite_db_path}'
            app.logger.warning(f"MySQL connection failed ({e}). Falling back to SQLite: {app.config['SQLALCHEMY_DATABASE_URI']}")

    # Ensure required directories exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(os.path.join(app.root_path, '..', 'instance'), exist_ok=True)
    os.makedirs(os.path.join(app.root_path, '..', 'logs'), exist_ok=True)

    # Initialize Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Register Flask-Login user loader
    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # Register Blueprints
    from app.dashboard import dashboard_bp
    from app.auth import auth_bp

    app.register_blueprint(dashboard_bp)
    app.register_blueprint(auth_bp)

    # Register Error Handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('500.html'), 500

    return app
