from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import SubmitField, StringField, PasswordField, BooleanField, FileField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    # TODO dynamically provide EN or DE labels
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class FileForm(FlaskForm):
    # TODO dynamically provide EN or DE labels
    file = FileField('Filename', validators=[FileRequired()])
    email_recipient = StringField('E-Mail Recipient', validators=[DataRequired()])
    submit = SubmitField('Deliver')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-Mail', validators=[DataRequired(), Email()])
    submit = SubmitField('Register')
