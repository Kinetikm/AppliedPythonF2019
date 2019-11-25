from flask import Flask

app = Flask(__name__)
app.config['DATABASE'] = 'sqlite:///database.db'
app.config['TEST_DATABASE'] = 'sqlite:///test.db'
