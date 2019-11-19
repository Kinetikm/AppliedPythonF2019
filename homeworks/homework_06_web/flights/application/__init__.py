from flask import Flask

app = Flask(__name__)
app.config['DATABASE'] = 'sqlite:///../flights.db'
app.config['TEST_DATABASE'] = 'sqlite:///test_flights.db'
