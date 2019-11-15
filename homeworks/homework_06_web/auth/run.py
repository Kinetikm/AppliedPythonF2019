from flask import Flask
from flask_login import LoginManager, UserMixin, login_required, current_user, login_user, logout_user
from marshmallow import Schema, fields, post_load
from application.model import Users

app = Flask(__name__)

app.config["SECRET_KEY"] = "123SECRET_KEY123"
app.config['REMEMBER_COOKIE_NAME'] = 'flight_board'

login_manager = LoginManager()
login_manager.init_app(app)


class RegistrationSchema(Schema):

    login = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True)


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))
