from app.database import db


class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    login = db.Column(db.String(100), nullable=False)
    passwd_hash = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return "<{}:{}>".format(self.user_id, self.email)


class Session(db.Model):
    __tablename__ = 'sessions'
    user_id = db.Column(db.Integer, primary_key=True)
    jwt_token = db.Column(db.String(300), nullable=False)
