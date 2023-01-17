from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, DateField, SelectField
from wtforms.validators import DataRequired, Email


# Registration Form
class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message="Please enter valid email.")])
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
    warm_up = CKEditorField('Warmup')
    fundamentals = CKEditorField('Fundamentals')
    music = CKEditorField('Music')
    goals = CKEditorField('Goals')
    submit = SubmitField("Save")
    cancel = SubmitField("Cancel")


class OrderForm(FlaskForm):
    order_by = SelectField('Order by', choices=[('desc', 'Most recent first'), ('asc', 'Oldest first'), ('created', 'Order Created')])

