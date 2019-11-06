from app import db


class Flight(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dept_time = db.Column(db.DateTime)
    arr_time = db.Column(db.DateTime)
    travel_time = db.Column(db.String(10))
    airport_id = db.Column(db.Integer, db.ForeignKey('airport.id'), nullable=False)
    aircraft_id = db.Column(db.Integer, db.ForeignKey('aircraft.id'), nullable=False)
    airports = db.relationship('Airport', backref='flights')
    aircrafts = db.relationship('Aircraft', backref='flights')

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
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(10))


class Airport(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30))


class Statistic(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.Integer, nullable=False)
    time = db.Column(db.Numeric(6, 4), nullable=False)
