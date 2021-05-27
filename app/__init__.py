from flask import Flask, render_template
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
mail = Mail()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)

    from .auth import blueprint as auth_blueprint
    from .delivery import blueprint as delivery_blueprint
    from .landing import blueprint as landing_blueprint

    @delivery_blueprint.app_errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500

    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(delivery_blueprint, url_prefix='/delivery')
    app.register_blueprint(landing_blueprint, url_prefix='/')

    return app
