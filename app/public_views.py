from app import app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user
from flask import render_template, redirect, url_for, flash
from app.forms import RegisterForm, LoginForm
from main import User


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            # User already exists
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))
        secured_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8)

        new_user = User(
            email=form.email.data,
            password=secured_password,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
        )
        db.session.add(new_user)
        db.session.commit()

        # This line will authenticate the user with Flask-Login
        login_user(new_user)
        return redirect(url_for('index'))
    return render_template("public/register.html", form=form, logged_in=current_user.is_authenticated)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        # Find user by email entered.
        user = User.query.filter_by(email=email).first()
        # Email doesn't exist
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        # Password incorrect
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        # Email exists and password correct
        else:
            login_user(user)
            return redirect(url_for('index'))
    return render_template("public/login.html", form=form, current_user=current_user, logged_in=current_user.is_authenticated)


@app.route("/", methods=["GET", "POST"])
def index():
    # print(app.config["DEBUG"])
    return render_template("public/index.html",  current_user=current_user, logged_in=current_user.is_authenticated)


@app.route("/faq", methods=["GET", "POST"])
def faq():
    return render_template("public/faq.html")
