from flask import Flask

from admin.view import admin_view
from auth.view import auth_view
from file.view import file_view


app = Flask(__name__)
app.config['MEMORY'] = {}
app.config['UPLOAD_FOLDER'] = '/tmp'

app.register_blueprint(admin_view, url_prefix='/admin')
app.register_blueprint(auth_view, url_prefix='/auth')
app.register_blueprint(file_view, url_prefix='/file')
