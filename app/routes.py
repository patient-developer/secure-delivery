from io import BytesIO

import flask_login
from PyPDF2 import PdfFileWriter, PdfFileReader
from flask import render_template, redirect, flash, url_for
from flask_login import login_user, login_required
from werkzeug.utils import secure_filename

from werkzeug.security import generate_password_hash

from app import app, db
from app.forms import LoginForm, FileForm, RegisterForm
from app.models import User, Permission
from config import Config
from .emails import send_mail
from .security import get_password


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(username=login_form.username.data).first()
        if user is None or not user.check_password(login_form.password.data):
            flash('Invalid username or password.')
            return redirect(url_for('login'))
        login_user(user, remember=login_form.remember_me.data)
        return redirect(url_for('delivery'))
    return render_template('login.html', form=login_form)


@app.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        u = flask_login.current_user
        if not u.role.permissions & Permission.REGISTER == Permission.REGISTER:
            flash('Not allowed to register users.')
            return redirect(url_for('login'))

        username = register_form.username.data
        password = get_password()

        user = User(username=username, password_hash=generate_password_hash(password), role_id=1)

        db.session.add(user)
        db.session.commit()

        send_mail('Password', Config.ADMINS[0], [register_form.email.data], password, None, None)

        return redirect(url_for('login'))
    return render_template('register.html', form=register_form)


@app.route('/delivery', methods=['GET', 'POST'])
@login_required
def delivery():
    file_form = FileForm()
    if file_form.validate_on_submit():
        password = get_password()
        filename = secure_filename(file_form.file.data.filename)

        out = PdfFileWriter()
        file = PdfFileReader(BytesIO(file_form.file.data.read()))

        for page in range(file.numPages):
            out.addPage(file.getPage(page))

        out.encrypt(password)

        attachment = BytesIO()

        out.write(attachment)

        send_mail('Attachment',
                  Config.ADMINS[0],
                  [file_form.email_recipient.data],
                  'Zustellung von ' + filename,
                  filename,
                  attachment.getvalue())

        send_mail('Password',
                  Config.ADMINS[0],
                  [file_form.email_recipient.data],
                  password, None, None)

        return redirect(url_for('delivery'))
    return render_template('delivery.html', form=file_form)
