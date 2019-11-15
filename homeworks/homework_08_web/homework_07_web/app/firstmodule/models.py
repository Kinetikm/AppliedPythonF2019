from app.database import db


class Plane(db.Model):
    __tablename__ = 'planes'
    plane_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(500), nullable=False)
    flights = db.relationship('Flight')

    def make_json_serializable(self):
        return {
            'plane': self.name
            }


class Airport(db.Model):
    __tablename__ = 'airports'
    airport_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(500), nullable=False)
    flights = db.relationship('Flight')

    def __repr__(self):
        return {
            'arrive_location': self.name
            }

    def make_json_serializable(self):
        return {
            'arrive_location': self.name
            }


class Flight(db.Model):
    __tablename__ = 'flights'
    flight_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    creator = db.Column(db.String(200), nullable=False)
    departure_time = db.Column(db.DateTime, nullable=False)
    arrival_time = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Time, nullable=False)
    arrive_airport = db.Column(db.Integer,
                               db.ForeignKey('airports.airport_id'),
                               nullable=False)
    plane = db.Column(db.Integer, db.ForeignKey('planes.plane_id'),
                      nullable=False)

    def make_json_serializable(self):
        return {
            'id': self.flight_id,
            'departure_time': str(self.departure_time),
            'arrival_time': str(self.arrival_time),
            'duration': str(self.duration)
            }


class Query(db.Model):
    __tablename__ = 'queries'
    query_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    query_time = db.Column(db.DateTime, nullable=False)
    answer_time = db.Column(db.Float(4), nullable=False)
    url = db.Column(db.String(200), index=True, nullable=False)
    method = db.Column(db.String(200), index=True, nullable=False)
    status_code = db.Column(db.Integer, nullable=False)

    def make_json_serializable(self):
        return {
            'query_id': self.query_id,
            'query_time': self.query_time,
            'answer_time': self.answer_time,
            'url': self.url,
            'method': self.method,
            'status_code': self.status_code
            }
