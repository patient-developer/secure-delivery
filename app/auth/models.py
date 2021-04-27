from app import db
from flask_login import UserMixin
from app import login
from werkzeug.security import check_password_hash


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    @staticmethod
    def insert_roles():
        roles = {
            RoleName.USER: [Permission.DELIVER],
            RoleName.ADMIN: [Permission.DELIVER, Permission.REGISTER]
        }
        default_role = 'User'
        for role in roles:
            db_role = Role.query.filter_by(name=role).first()
            if db_role is None:
                db_role = Role(name=role)
            db_role.reset_permissions()
            for perm in roles[role]:
                db_role.add_permission(perm)
            db_role.default = (db_role.name == default_role)
            db.session.add(db_role)
        db.session.commit()


class Permission:
    DELIVER = 1
    REGISTER = 2


class RoleName:
    USER = 'User'
    ADMIN = 'Admin'
