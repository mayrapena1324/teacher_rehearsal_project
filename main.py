from app import app
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor

ckeditor = CKEditor(app)
Bootstrap(app)
# ##CONNECT TO DB
db = SQLAlchemy(app)  # configuration in config files

# CONFIGURE FLASK_LOGIN
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


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


# with app.app_context():
#     db.create_all()

# adding a comment for my first branch test for test_branch

if __name__ == '__main__':
    app.run()
