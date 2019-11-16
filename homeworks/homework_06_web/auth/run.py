from flask import Flask, request, g, abort
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from marshmallow import Schema, fields, ValidationError, validates_schema
from application.model import Users, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

app.config["SECRET_KEY"] = "123SECRET_KEY123"
app.config['REMEMBER_COOKIE_NAME'] = 'flight_board'

engine = create_engine('sqlite:///../flights.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


login_manager = LoginManager()
login_manager.init_app(app)


def get_db():
    if 'db' not in g:
        g.db = Session()

    return g.db


class RegistrationSchema(Schema):

    login = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True)


class LoginSchema(Schema):

    login = fields.String(required=True)
    password = fields.String(required=True)


@login_manager.user_loader
def load_user(user_id):
    session = get_db()
    return session.query(Users).get(int(user_id))


@app.route('/registration', methods=['POST'])
def registration():
    try:
        schema = RegistrationSchema()
        data = schema.load(request.json)
        session = get_db()
        if session.query(Users).filter(Users.username == data['login']).first():
            abort(400, 'User exist')
        user = Users(username=data['login'], email=data['email'])
        user.set_password(data['password'])

        session.add(user)
        session.commit()
        return 'OK'
    except ValidationError as e:
        abort(400, str(e))


@app.route('/login', methods=['POST'])
def login():
    try:
        data = LoginSchema().load(request.json)
        session = get_db()
        user = session.query(Users).filter(Users.username==data['login']).first()
        if not user.check_password(data['password']):
            abort(401)
        login_user(user, remember=True)
        return '', 204
    except ValidationError as e:
        abort(400, str(e))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return '', 204


@app.route('/check')
@login_required
def check():
    return 'OK'


@app.teardown_appcontext
def teardown_db(args):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def main():
    app.run(host='localhost', debug=True)


if __name__ == '__main__':
    main()
