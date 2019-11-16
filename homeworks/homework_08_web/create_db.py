from orm import Flights, Dest_airports, Aircraft_types, User_database, Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


engine = create_engine('sqlite:///database.db')
if __name__ == "__main__":
    flights = [{
            "departure": "7:31",
            "arrival": "13:44",
            "travel_time": "6:13",
            "destination": "Riyadh",
            "aircraft_type": "Snoop-Dog Airbus A320"
        },
        {
            "departure": "22:31",
            "arrival": "6:44",
            "travel_time": "8:13",
            "destination": "Tokyo",
            "aircraft_type": "Syknoi SuperJet"
        },
        {
            "departure": "20:31",
            "arrival": "5:44",
            "travel_time": "9:13",
            "destination": "Jamaica",
            "aircraft_type": "Airbus 9000"
    }]
    user = {
        "token": 'toekrrtgg234234-tkfdgmgkd543',
        "login": 'login1',
        "password": 'password',
        "email": "testin@mail.ru"
    }
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    for flight in flights:
        ap = Dest_airports(airport=flight["destination"])
        ac = Aircraft_types(aircraft=flight["aircraft_type"])
        session.add(ap)
        session.add(ac)
        session.commit()
        f = Flights(departure=flight["departure"],
                    arrival=flight["arrival"],
                    travel_time=flight["travel_time"],
                    airport_id=ap.id,
                    aircraft_id=ac.id)
        session.add(f)
        session.commit()
    ur = User_database(
            login=user["login"],
            password=user["password"],
            token=user["token"],
            email=user["email"])
    session.add(ur)
    session.commit()
    session.close()
