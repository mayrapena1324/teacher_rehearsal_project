from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user


# configure flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET_APP_KEY'
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
    name = db.Column(db.String(250), nullable=False)


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/rehearsal", methods=["GET", "POST"])
def rehearsal():
    return render_template("rehearsal.html")


@app.route("/faq", methods=["GET", "POST"])
def faq():
    return render_template("faq.html")


if __name__ == '__main__':
    app.run(port=5000, debug=True)
