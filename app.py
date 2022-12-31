from flask import Flask, render_template, redirect, url_for, request, flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from functools import wraps
from flask import abort
from forms import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash

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


# with app.app_context():
#     db.create_all()

# Create admin-only decorator
def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.id != 1:
            return abort(403)
        # Otherwise, continue with the route function
        return f(*args, **kwargs)

    return decorated_function


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
            name=form.name.data,
        )
        db.session.add(new_user)
        db.session.commit()

        # This line will authenticate the user with Flask-Login
        login_user(new_user)
        return redirect(url_for('index'))
    return render_template("register.html", form=form, logged_in=current_user.is_authenticated)


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
    return render_template("login.html", form=form, current_user=current_user, logged_in=current_user.is_authenticated)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html",  current_user=current_user, logged_in=current_user.is_authenticated)


@app.route("/rehearsal", methods=["GET", "POST"])
def rehearsal():
    return render_template("rehearsal.html")


@app.route("/faq", methods=["GET", "POST"])
def faq():
    return render_template("faq.html")


if __name__ == '__main__':
    app.run(port=5000, debug=True)
