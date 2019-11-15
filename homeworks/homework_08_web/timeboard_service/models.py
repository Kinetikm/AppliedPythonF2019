from timeboard_service import db
import json


class FlightTable(db.Model):
    __tablename__ = 'flight'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dep_time = db.Column(db.Integer, nullable=False)
    arr_time = db.Column(db.Text, nullable=False)
    travel_time = db.Column(db.Text, nullable=False)
    creator = db.Column(db.Text, nullable=False)

    aircraft_id = db.Column(db.Integer, db.ForeignKey('aircraft.id'), nullable=False)
    dst_airport_id = db.Column(db.Integer, db.ForeignKey('dst_airport.id'), nullable=False)
    aircraft = db.relationship('AircraftTable')
    dst_airport = db.relationship('AirportTable')

    def get_info(self):
        return {
            'id': self.id,
            'dep_time': self.dep_time,
            'arr_time': self.arr_time,
            'aircraft': self.aircraft.name,
            'dst_airport': self.dst_airport.name,
            'travel_time': self.travel_time,
            'creator': self.creator
        }

    def __repr__(self):
        return json.dumps({
            'id': self.id
        })


class AircraftTable(db.Model):
    __tablename__ = 'aircraft'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    flights = db.relationship('FlightTable', backref='aircrafttable', lazy=True)

    def __repr__(self):
        return json.dumps({
            'id': self.id,
            'name': self.name,
            'flights': [{'id': flight.id} for flight in self.flights]
        })


class AirportTable(db.Model):
    __tablename__ = 'dst_airport'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    flights = db.relationship('FlightTable', backref='airporttable', lazy=True)

    def __repr__(self):
        return json.dumps({
            'id': self.id,
        })


class StatisticTable(db.Model):
    __tablename__ = 'statistic'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    req_type = db.Column(db.Integer, nullable=False)
    time = db.Column(db.Numeric(5, 3), nullable=False)

    def __repr__(self):
        return json.dumps({
            'id': self.id
        })
