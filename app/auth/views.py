import flask_login
from flask import url_for, render_template, flash, request
from flask_login import login_required, login_user, logout_user
from werkzeug.security import generate_password_hash
from werkzeug.utils import redirect
from werkzeug.urls import url_parse

from . import blueprint
from .. import db
from .forms import RegisterForm, LoginForm
from .models import User, Permission
from ..emails import send_mail
from ..security import get_password
from config import Config


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(username=str(login_form.username.data).strip()).first()
        if user is None or not user.check_password(str(login_form.password.data).strip()):
            flash('Invalid username or password.')
            return redirect(url_for('.login'))
        login_user(user, remember=login_form.remember_me.data)
        flash('Successfully signed in.')
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('landing.index')
        return redirect(next_page)
    return render_template('login.html', form=login_form)


@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('landing.index'))


@blueprint.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    u = flask_login.current_user
    if not u.role.permissions & Permission.REGISTER == Permission.REGISTER:
        flash('Not allowed to register users.')
        return redirect(url_for('landing.index'))

    register_form = RegisterForm()
    if register_form.validate_on_submit():
        username = str(register_form.username.data).strip()
        password = get_password()

        user = User(username=username, password_hash=generate_password_hash(password), role_id=1)

        db.session.add(user)
        db.session.commit()

        recipient = register_form.email.data

        send_mail('Benutzername', Config.ADMINS[0], [recipient], welcome_message(username), None, None)
        send_mail('Password', Config.ADMINS[0], [recipient], password_message(password), None, None)

        flash('Successfully registered user {} and sent password to {}'.format(username, recipient))
        return redirect(url_for('landing.index'))
    return render_template('register.html', form=register_form)


def welcome_message(username: str):
    return 'Hallo,\n\nvielen Dank, dass Sie Verschluesselter Anhang nutzen auf\n\n  {}{}\n\n' \
           'Sie haben den Benuternamen\n\n {}\n\nSie erhalten in Kuerze per E-Mail Ihr Passwort.' \
        .format(Config.BASE_URL, url_for('landing.index'), username)


def password_message(password: str):
    return 'Hallo,\n\nanbei Ihr Passwort\n\n  {}\n\nSie koennen sich nun anmelden unter\n\n {}{}' \
        .format(password, Config.BASE_URL, url_for('auth.login'))
