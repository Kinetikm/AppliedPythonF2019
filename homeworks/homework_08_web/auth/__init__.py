from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app_auth = Flask(__name__)
app_auth.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app_auth.config["SECRET_KEY"] = "123SECRET_KEY123"
db = SQLAlchemy(app_auth)

login_manager = LoginManager()
login_manager.init_app(app_auth)

from auth.database import fill_database

fill_database(db)
