from auth_service import db
import json
from flask_login import UserMixin


class UsersTable(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(50), unique=True, index=True, nullable=False)
    email = db.Column(db.String(100), nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)

    cookie = db.relationship('CookiesTable')

    def __repr__(self):
        return json.dumps({
            'id': self.id
        })


class CookiesTable(db.Model):
    __tablename__ = 'cookies'
    myid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    token = db.Column(db.String(100), unique=True, nullable=False)
    expire = db.Column(db.String(100), unique=True, nullable=False)

    user = db.relationship('UsersTable')

    def __repr__(self):
        return json.dumps({
            'id': self.myid
        })
