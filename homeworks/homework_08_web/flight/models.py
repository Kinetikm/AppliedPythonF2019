from flight import db
from flask_login import UserMixin


class Flight(db.Model):
    id_flight = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dept_time = db.Column(db.DateTime)
    arr_time = db.Column(db.DateTime)
    travel_time = db.Column(db.String(10))
    owner = db.Column(db.Integer, db.ForeignKey('user.id_user'), nullable=False)
    airport_id = db.Column(db.Integer, db.ForeignKey('airport.id_airport'), nullable=False)
    aircraft_id = db.Column(db.Integer, db.ForeignKey('aircraft.id_aircraft'), nullable=False)
    airports = db.relationship('Airport', backref='flights')
    aircrafts = db.relationship('Aircraft', backref='flights')

    def check_user(self, user_id):
        return self.owner == user_id

    def in_dict(self):
        result = {
            'Id': self.id,
            'Departure time': self.dept_time,
            'Arrival time': self.arr_time,
            'Travel time': self.travel_time,
            'Aircraft': self.aircrafts.query.get(self.aircraft_id).name,
            'Airport': self.airports.query.get(self.airport_id).name
        }
        return result


class Aircraft(db.Model):
    id_aircraft = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(10))


class Airport(db.Model):
    id_airport = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30))


class Statistic(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.Integer, nullable=False)
    time = db.Column(db.Numeric(6, 4), nullable=False)


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id_user = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(20))
    password = db.Column(db.String(70))
    email = db.Column(db.String(50))
    cookie = db.Column(db.String(100))
