# make our app a package
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()
db = SQLAlchemy()
ckeditor = CKEditor()


def create_app():
    app = Flask(__name__)

    if app.config["DEBUG"]:
        app.config.from_object("config.DevelopmentConfig")

    else:
        app.config.from_object("config.Config")

    Bootstrap(app)
    db.init_app(app)
    ckeditor.init_app(app)
    csrf.init_app(app)

    with app.app_context():
        from . import user_views, public_views, error_handlers, auth, models  # Import routes
        create_database()
        return app


# create the database
def create_database():
    if not path.exists("teacher_rehearsal_project/instance/rehearsify.db"):
        db.create_all()  # Create sql tables for our data models
        print("Created Database!")