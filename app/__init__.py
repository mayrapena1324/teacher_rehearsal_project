# make our app a package
from flask import Flask

app = Flask(__name__)

if app.config["DEBUG"]:
    app.config.from_object("config.DevelopmentConfig")

else:
    app.config.from_object("config.Config")

# importing views files to avoid a circular import
from app import public_views
from app import admin_views  # import admin views
from app import user_views
