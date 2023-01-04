# make our app a package
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager
from flask_ckeditor import CKEditor


app = Flask(__name__)

if app.config["DEBUG"]:
    app.config.from_object("config.DevelopmentConfig")

else:
    app.config.from_object("config.Config")

ckeditor = CKEditor(app)
Bootstrap(app)

##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///rehearsify.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# CONFIGURE FLASK_LOGIN
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


##  Configure Tables
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250))
    first_name = db.Column(db.String(250), nullable=False)
    last_name = db.Column(db.String(250), nullable=False)


class Rehearsal(db.Model):
    __tablename__ = "rehearsals"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, unique=True, nullable=False)
    warm_up = db.Column(db.Text, nullable=True)
    fundamentals = db.Column(db.Text, nullable=True)
    music = db.Column(db.Text, nullable=True)


# This will store the uploads a user makes. Need to be tied to rehearsal? or user?
# class Upload(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     filename = db.Column(db.String(50))
#     data = db.Column(db.LargeBinary)

with app.app_context():
    db.create_all()

# importing views files to avoid a circular import
from app import public_views
from app import admin_views  # import admin views
from app import user_views
