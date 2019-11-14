import os
from flask import Flask
from .database import db
import app.firstmodule.models
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)


def create_app():
    app = Flask(__name__)
    app.config.from_object(os.environ['AUTH_SETTINGS'])
    db.init_app(app)
    jwt = JWTManager(app)
    with app.test_request_context():
        db.create_all()
    import app.firstmodule.controllers as firstmodule
    app.register_blueprint(firstmodule.module)
    return app