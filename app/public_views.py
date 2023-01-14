from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user
from flask import render_template, redirect, url_for, flash
from app.forms import RegisterForm, LoginForm
from .models import db, User


@app.route("/", methods=["GET", "POST"])
def index():

    return render_template("public/index.html",  current_user=current_user, logged_in=current_user.is_authenticated)


@app.route("/faq", methods=["GET", "POST"])
def faq():
    return render_template("public/faq.html", current_user=current_user, logged_in=current_user.is_authenticated)
