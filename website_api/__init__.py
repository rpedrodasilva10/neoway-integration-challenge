import os
from flask import Flask
from .extensions import db


def create_app():
    """Construct the core application."""
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    with app.app_context():
        # Imports
        from . import views

        # Create tables for our models
        db.create_all()

        return app
