from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Time
from sqlalchemy.ext.declarative import declarative_base
import datetime
from os import path
from sqlalchemy import create_engine, select, and_
from sqlalchemy import ForeignKey, PrimaryKeyConstraint, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, relationship
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash
import sys
import os

engine = create_engine('sqlite:///database.db')
session = Session(bind=engine)
Base = declarative_base()


class User_database(Base):
    __tablename__ = 'user_database'
    id = Column(Integer, primary_key=True)
    login = Column(String(20), unique=True)
    email = Column(String(30))
    password_hash = db.Column(db.String(100), nullable=False)

    def deserializ(self):
        result = (self.login, self.password, self.email)
        return result

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,  password):
        return check_password_hash(self.password_hash, password)


def get_user(token):
    user = session.query(User_database).filter(User_database.token == token).first()
    if user:
        return user.deserializ(), True
    else:
        None, False


def set_user(token, data):
    userdb = User_database(
                    login=data["login"],
                    password=data["password"],
                    email=data["email"],
                    token=token)
    session.add(flightdb)
    session.commit()
    return True