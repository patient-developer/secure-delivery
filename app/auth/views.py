import flask_login
from flask import url_for, render_template, flash
from flask_login import login_required, login_user
from werkzeug.security import generate_password_hash
from werkzeug.utils import redirect

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
        user = User.query.filter_by(username=login_form.username.data).first()
        if user is None or not user.check_password(login_form.password.data):
            flash('Invalid username or password.')
            return redirect(url_for('login'))
        login_user(user, remember=login_form.remember_me.data)
        return redirect(url_for('delivery'))
    return render_template('login.html', form=login_form)


@blueprint.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        u = flask_login.current_user
        if not u.role.permissions & Permission.REGISTER == Permission.REGISTER:
            flash('Not allowed to register users.')
            return redirect(url_for('.login'))

        username = register_form.username.data
        password = get_password()

        user = User(username=username, password_hash=generate_password_hash(password), role_id=1)

        db.session.add(user)
        db.session.commit()

        send_mail('Password', Config.ADMINS[0], [register_form.email.data], password, None, None)

        return redirect(url_for('.login'))
    return render_template('register.html', form=register_form)
