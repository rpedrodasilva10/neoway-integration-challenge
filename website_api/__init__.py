import os
from flask import Flask
from .extensions import db


def create_app(config_name):
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    # app.config.from_pyfile('config.py')
    app.config.from_object(config_name)
    db.init_app(app)

    with app.app_context():
        # Imports
        from . import views

        # Create tables for our models
        db.create_all()

        return app
