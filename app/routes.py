from flask import render_template, redirect, flash, url_for
from flask_login import login_user, login_required

from werkzeug.utils import secure_filename

from app import app
from app.forms import LoginForm, FileForm
from app.models import User

from .emails import send_mail

from config import Config


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(username=login_form.username.data).first()
        if user is None or not user.check_password(login_form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=login_form.remember_me.data)
        return redirect(url_for('delivery'))
    return render_template('login.html', form=login_form)


@app.route('/delivery', methods=['GET', 'POST'])
@login_required
def delivery():
    file_form = FileForm()
    if file_form.validate_on_submit():
        flash('Will deliver ' + file_form.file.name)
        filename = secure_filename(file_form.file.data.filename)
        send_mail(
            '!!! TEST !!!',
            Config.ADMINS[0],
            [file_form.email_recipient.data],
            'Zustellung von ' + filename,
            filename,
            file_form.file.data.read())
        return redirect(url_for('delivery'))
    return render_template('delivery.html', form=file_form)
