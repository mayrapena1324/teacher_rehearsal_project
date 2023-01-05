# make our app a package
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    if app.config["DEBUG"]:
        app.config.from_object("config.DevelopmentConfig")

    else:
        app.config.from_object("config.Config")

    db.init_app(app)

    with app.app_context():
        from . import user_views, public_views  # Import routes
        db.create_all()  # Create sql tables for our data models

        return app

# importing views files to avoid a circular import
from app import public_views
from app import admin_views  # import admin views
from app import user_views
