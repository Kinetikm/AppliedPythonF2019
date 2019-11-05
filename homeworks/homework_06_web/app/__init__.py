import os
from flask import Flask
from .database import db
import app.firstmodule.models


def create_app():
    app = Flask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])
    db.init_app(app)
    with app.test_request_context():
        db.create_all()
    import app.firstmodule.controllers as firstmodule
    app.register_blueprint(firstmodule.module)
    return app
