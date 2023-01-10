"""Data models."""
from flask_login import UserMixin, LoginManager

from . import db

from flask import current_app as app


#  Configure Tables
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
    # goals = db.Column(db.Text, nullable=True)
    #title ??? add class ?


# CONFIGURE FLASK_LOGIN
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
