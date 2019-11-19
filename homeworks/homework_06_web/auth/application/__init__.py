from flask import Flask
import sys

app = Flask(__name__)
app.config['DATABASE'] = 'sqlite:///../flights.db'
app.config['TEST_DATABASE'] = 'sqlite:///test_auth.db'
