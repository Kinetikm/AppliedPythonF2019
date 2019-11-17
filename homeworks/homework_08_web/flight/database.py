from flight.models import *
from datetime import datetime


def fill_database(db):
    db.create_all()

    airports = [Airport(name="MOS"), Airport(name="VNG"), Airport(name="CSO")]
    aircrafts = [Aircraft(name="SU180"), Aircraft(name="DE830"), Aircraft(name="VN370")]
    db.session.add_all(airports)
    db.session.add_all(aircrafts)
    db.session.flush()

    flights = [
        Flight(
            dept_time=datetime.strptime("2019-09-21 13:00+0000", '%Y-%m-%d %H:%M%z'),
            arr_time=datetime.strptime("2019-09-21 15:00+0000", '%Y-%m-%d %H:%M%z'),
            travel_time="02:00",
            owner=1,
            airport_id=airports[0].id_airport,
            aircraft_id=aircrafts[0].id_aircraft
        ),
        Flight(
            dept_time=datetime.strptime("2015-02-21 18:00+0000", '%Y-%m-%d %H:%M%z'),
            arr_time=datetime.strptime("2015-02-21 21:00+0000", '%Y-%m-%d %H:%M%z'),
            travel_time="03:00",
            owner=1,
            airport_id=airports[1].id_airport,
            aircraft_id=aircrafts[1].id_aircraft
        ),
        Flight(
            dept_time=datetime.strptime("2019-01-24 01:00+0000", '%Y-%m-%d %H:%M%z'),
            arr_time=datetime.strptime("2019-01-24 03:00+0000", '%Y-%m-%d %H:%M%z'),
            travel_time="02:00",
            owner=1,
            airport_id=airports[2].id_airport,
            aircraft_id=aircrafts[2].id_aircraft
        )
    ]
    db.session.add_all(flights)
    db.session.commit()
