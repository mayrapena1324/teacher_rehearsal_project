from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, DateField
from wtforms.validators import DataRequired, URL


# Registration Form
class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    submit = SubmitField("Register")


# Login form
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')


# Rehearsal Form
class RehearsalForm(FlaskForm):
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    group = StringField('Group', validators=[DataRequired()])
    warm_up = CKEditorField('Warm up', validators=[DataRequired()])
    fundamentals = CKEditorField('Fundamentals', validators=[DataRequired()])
    music = CKEditorField('Music', validators=[DataRequired()])
    goals = CKEditorField('Goals', validators=[DataRequired()])
    submit = SubmitField("Save")
    cancel = SubmitField("Cencel")
