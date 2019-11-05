from app.database import db
import app.firstmodule.models as models
import time
import numpy as np


def get_by_attr(table, attr, value):
    """
    Checks existance of attribute in table
    """
    return db.session.query(table).filter(attr == value).all()


def add_flight(request):
    plane = None
    airport = None
    try:
        plane = (db.session.query(models.Plane)
                 .filter(models.Plane.name == request
                         .json['aircraft_type']).all()[0])
        airport = (db.session.query(models.Airport)
                   .filter(models.Airport.name == request
                           .json['arrive_location']).all()[0])
    except IndexError:
        pass
    if not plane:
        plane = models.Plane(name=request.json['aircraft_type'])
        db.session.add(plane)
        db.session.commit()
    if not airport:
        airport = models.Airport(name=request.json['arrive_location'])
        db.session.add(airport)
        db.session.commit()
    new_flight = models.Flight(
        departure_time=request.json['departure_time'],
        arrival_time=request.json['arrival_time'],
        duration=request.json['duration'],
        arrive_airport=airport.airport_id,
        plane=plane.plane_id
        )
    db.session.add(new_flight)
    db.session.commit()


def get_all_flights(params):
    if not params.get('filter'):
        q = (db.session.query(models.Flight, models.Plane, models.Airport)
             .filter(models.Flight.plane ==
                     models.Plane.plane_id)
             .filter(models.Flight.arrive_airport ==
                     models.Airport.airport_id).all())
    else:
        q = (db.session.query(models.Flight, models.Plane, models.Airport)
             .filter(models.Flight.plane == models.Plane.plane_id)
             .filter(models.Flight.arrive_airport == models.Airport.airport_id)
             .filter(models.Airport.name == params['filter'])
             .all())
    all_flights = []
    for el in q:
        dict_ = el[0].make_json_serializable()
        dict_.update(el[2].make_json_serializable())
        dict_.update(el[1].make_json_serializable())
        all_flights.append(dict_)
    if not params.get('sorted'):
        return all_flights
    else:
        all_flights_sorted = sorted(all_flights, key=lambda flight:
                                    flight['duration'], reverse=True)
        return all_flights_sorted


def get_flight_by_id(flight_id):
    res = (db.session.query(models.Flight, models.Plane, models.Airport)
           .filter(models.Flight.plane == models.Plane.plane_id)
           .filter(models.Flight.arrive_airport == models.Airport.airport_id)
           .filter(models.Flight.flight_id == flight_id)
           .all())
    res = res[0]
    dict_ = res[0].make_json_serializable()
    dict_.update(res[2].make_json_serializable())
    dict_.update(res[1].make_json_serializable())
    return dict_


def modify_flight(request, flight_id, flight):
    plane = get_by_attr(models.Plane, models.Plane.name,
                        request.json['aircraft_type'])[0]
    airport = get_by_attr(models.Airport, models.Airport.name,
                          request.json['arrive_location'])[0]
    flight.departure_time = request.json['departure_time']
    flight.arrival_time = request.json['arrival_time']
    flight.duration = request.json['duration']
    flight.arrive_airport = airport.airport_id
    flight.plane = plane.plane_id
    db.session.commit()


def get_flight_object(flight_id):
    return db.session.query(models.Flight).filter(models.Flight.flight_id ==
                                                  flight_id)


def delete_flight(flight_id):
    db.session.query(models.Flight).filter(models.Flight.flight_id ==
                                           flight_id).delete()
    db.session.commit()


def add_metric(request, query_time, answer_time, status_code):
    converted_query_time = time.strftime('%Y-%m-%d %H:%M:%S',
                                         time.gmtime(query_time))
    query = models.Query(query_time=converted_query_time,
                         answer_time=answer_time, url=request.url,
                         method=request.method, status_code=status_code)
    db.session.add(query)
    db.session.commit()


def get_metrix(params):
    qry = (db.session.query(db.func.min(models.Query.answer_time))
           .filter(models.Query.method == params['method']))
    res_dict = {'min answer time': qry[0]}
    qry = (db.session.query(db.func.avg(models.Query.answer_time))
           .filter(models.Query.method == params['method']))
    res_dict.update({'average answer time': qry[0]})
    qry = (db.session.query(db.func.count(models.Query.answer_time))
           .filter(models.Query.method == params['method']))
    res_dict.update({'such queries num': qry[0]})
    qry = (db.session.query(models.Query.answer_time)
           .filter(models.Query.method == params['method']))
    arr = np.array([])
    for el in qry:
        arr = np.append(arr, [el])
    perc = np.percentile(arr, 0.9)
    res_dict.update({'0.9 percentile': float('{:.5f}'.format(perc))})
    return res_dict
