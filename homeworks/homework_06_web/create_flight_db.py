import datetime
import random
from app.model import Base, Airports, Airplanes, Flights
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
flights_engine = create_engine('sqlite:///flights.db')


def generate_data(n=5, start_date=datetime.datetime(2018, 1, 1, tzinfo=datetime.timezone.utc),
                  end_date=datetime.datetime(2019, 1, 1, tzinfo=datetime.timezone.utc),
                  max_flight_time=10):
    data = []
    airports = ['Moscow', 'Chelyabinsk', 'Ekaterinburg', 'London', 'Berlin', 'Minsk']
    planes = ['A320', 'B777', 'B737', 'A319', 'A380']
    for i in range(n):
        # генерируем случайное время отправления и прибытия
        delta = end_date - start_date
        int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
        random_second = random.randrange(int_delta)
        t1 = start_date + datetime.timedelta(seconds=random_second)
        t2 = t1 + datetime.timedelta(hours=random.randrange(max_flight_time)+1)
        h = (t2 - t1).seconds // 3600
        m = (t2 - t1).seconds // 60 % 60
        d = {'dep_time': t1, 'arr_time': t2, 'dest_airport': random.randint(1, len(airports)),
             'airplane': random.randint(1, len(planes)),
             'flight_time': '{h}:{m}'.format(h=h, m=m)}
        data.append(d)
    Base.metadata.create_all(flights_engine)
    Session = sessionmaker(bind=flights_engine)
    session = Session()
    for airport in airports:
        a = Airports(airport=airport)
        session.add(a)
    for plane in planes:
        p = Airplanes(airplane=plane)
        session.add(p)
    for d in data:
        entry = Flights(dep_time=d['dep_time'], arr_time=d['arr_time'], airport_id=d['dest_airport'],
                        plane_id=d['airplane'], flight_time=d['flight_time'])
        session.add(entry)
    session.commit()
    for i in session.query(Flights).all():
        print(i.id, i.serialize)
    session.close()


if __name__ == "__main__":
    generate_data()
