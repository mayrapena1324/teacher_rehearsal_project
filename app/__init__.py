# make our app a package
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
ckeditor = CKEditor()


def create_app():
    app = Flask(__name__)

    if app.config["DEBUG"]:
        app.config.from_object("config.DevelopmentConfig")

    else:
        app.config.from_object("config.Config")

    db.init_app(app)
    ckeditor.init_app(app)
    Bootstrap(app)

    with app.app_context():
        from . import user_views, public_views, error_handlers, auth  # Import routes
        db.create_all()  # Create sql tables for our data models

        return app

