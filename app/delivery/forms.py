from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import FileField, StringField, SubmitField
from wtforms.validators import DataRequired, Email


class FileForm(FlaskForm):
    file = FileField('Filename', validators=[FileRequired()])
    email_recipient = StringField('E-Mail Recipient', validators=[DataRequired(), Email()])
    submit = SubmitField('Deliver')
