from timeboard_service.utils.validation_schema import FlightSchema
from timeboard_service.models import FlightTable, AircraftTable, AirportTable
from timeboard_service.utils.exception import ApiException
from timeboard_service import db


def show_all(offset, limit, dep_time):
    if dep_time is None:
        flights = FlightTable.query.offset(offset).limit(limit).all()
    else:
        flights = FlightTable.query.offset(offset).limit(limit).filter_by(dep_time=dep_time).all()

    return [flight.get_info() for flight in flights]


def add_flight(body):
    FlightSchema().load(body)

    aircraft = AircraftTable.query.filter_by(name=body["aircraft"]).first()
    if aircraft is None:
        raise ApiException(400, "Data incorrect", "Aircraft doesnt exist")

    dst_airport = AirportTable.query.filter_by(name=body["dst_airport"]).first()
    if dst_airport is None:
        raise ApiException(400, "Data incorrect", "Airport doesnt exist")

    fl = FlightTable(
        dep_time=body['dep_time'],
        arr_time=body['arr_time'],
        travel_time=body['travel_time'],
        dst_airport_id=dst_airport.id,
        aircraft_id=aircraft.id
    )

    aircraft.flights.append(fl)
    dst_airport.flights.append(fl)
    db.session.add(fl)
    db.session.commit()

    return fl.get_info()


def show_flight(_id):
    flight = FlightTable.query.filter_by(id=_id).first()
    if flight is None:
        raise ApiException(404, "Index out of range", "Flight with such ID doesnt exist")

    return flight.get_info()


def update_flight(body, _id):
    FlightSchema().load(body)
    if _id != body['id']:
        raise ApiException(404, "Bad index", "Index from URL and body are different")

    flight = FlightTable.query.filter_by(id=_id).first()
    if flight is None:
        raise ApiException(404, "Index out of range", "Flight with such ID doesnt exist")

    aircraft = AircraftTable.query.filter_by(name=body["aircraft"]).first()
    if aircraft is None:
        raise ApiException(400, "Data incorrect", "Aircraft doesnt exist")

    dst_airport = AirportTable.query.filter_by(name=body["dst_airport"]).first()
    if dst_airport is None:
        raise ApiException(400, "Data incorrect", "Airport doesnt exist")

    flight.dep_time = body['dep_time']
    flight.arr_time = body['arr_time']
    flight.travel_time = body['travel_time']

    if flight.get_info()['aircraft'] != body['aircraft']:
        flight.aircraft_id = aircraft.id

    if flight.get_info()['dst_airport'] != body['dst_airport']:
        flight.dst_airport_id = dst_airport.id

    db.session.commit()
    return flight.get_info()


def del_flight(_id):
    flight = FlightTable.query.filter_by(id=_id).first()
    if flight is None:
        raise ApiException(404, "Index out of range", "Flight with such ID doesnt exist")

    db.session.delete(flight)
    db.session.commit()
    return
