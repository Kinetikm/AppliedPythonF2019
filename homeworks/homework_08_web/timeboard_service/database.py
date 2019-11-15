def init_db(db):
    from timeboard_service.models import FlightTable, AircraftTable, AirportTable

    aircrafts = []
    aircraft_names = ["Boeing", "Airbus", "Superjet"]
    for name in aircraft_names:
        aircraft = AircraftTable(
            name=name
                             )
        aircrafts.append(aircraft)

    airports = []
    airport_names = ["VOL", "CAN", "SEP"]
    for name in airport_names:
        aiport = AirportTable(
            name=name
                             )
        airports.append(aiport)

    flights = []
    dep_time = ["10:00", "11:00", "12:00"]
    arr_time = ["11:00", "12:00", "13:00"]
    travel_time = ["1H00M", "1H00M", "1H00M"]
    creator = ["creat", "pos", "kon"]
    for d_time, a_time, t_time, cr in zip(dep_time, arr_time, travel_time, creator):
        flight = FlightTable(
            dep_time=d_time,
            arr_time=a_time,
            travel_time=t_time,
            creator=cr
                             )
        flights.append(flight)

    i = 1
    for flight in flights:
        aircrafts[i % 3].flights.append(flight)
        airports[i % 3].flights.append(flight)
        i += 1

    db.session.add_all(airports)
    db.session.add_all(aircrafts)
    db.session.add_all(flights)
    db.session.commit()
