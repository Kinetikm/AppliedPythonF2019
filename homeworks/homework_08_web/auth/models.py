from auth import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


@login_manager.user_loader
def load_user(login):
    return db.session.query(User).filter(User.login == login).first()


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id_user = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(20))
    password = db.Column(db.String(70))
    email = db.Column(db.String(50))
    cookie = db.Column(db.String(100))

    def get_id(self):
        return self.login

    @classmethod
    def get(cls, login):
        user = User.query.filter_by(login=login).first()
        if not user:
            return
        return user

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
