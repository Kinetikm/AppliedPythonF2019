from flask import Flask, jsonify, request
import sqlite3
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
conn = sqlite3.connect('auth.db')
c = conn.cursor()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///auth.db'
db = SQLAlchemy(app)


class Cookies(db.Model):
    __tablename__ = 'Cookies'
    username = db.Column(db.String(), primary_key=True)
    email = db.Column(db.String())
    password = db.Column(db.String())
    cookie = db.Column(db.String())

db.drop_all()
db.create_all()
