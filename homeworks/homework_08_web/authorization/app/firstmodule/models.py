from app.database import db


class User(db.Model):
    __tablename__ = 'users'
    email = db.Column(db.String(100), nullable=False)
    login = db.Column(db.String(100), nullable=False, primary_key=True)
    passwd_hash = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return "<{}:{}>".format(self.user_id, self.email)


class Session(db.Model):
    __tablename__ = 'sessions'
    login = db.Column(db.String(100), primary_key=True)
    jwt_token = db.Column(db.String(500), nullable=False)
