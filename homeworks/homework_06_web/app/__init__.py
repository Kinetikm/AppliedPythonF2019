from flask import Flask


def create_app():
    app = Flask(__name__)
    import app.firstmodule.controllers as firstmodule
    app.register_blueprint(firstmodule.module)
    return app
