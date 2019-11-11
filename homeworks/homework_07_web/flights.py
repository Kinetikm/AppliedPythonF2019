from sqlalchemy import create_engine, MetaData, Table,\
    Column, Integer, String, ForeignKey, select
from sqlalchemy.orm import sessionmaker, relationship, scoped_session

engine = create_engine('sqlite:///C:\sqlitedbs\database.db', echo=True)
from sqlalchemy.sql.expression import update

from sqlalchemy.ext.declarative import declarative_base

session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()


class Flights(Base):
    __tablename__ = 'flights'
    id = Column(Integer, primary_key=True)
    f_id = Column(Integer)
    departure = Column(String)
    arrival = Column(String)
    flight_time = Column(String)
    airport_id = Column(String, ForeignKey('airports.id'))
    plane_id = Column(String, ForeignKey('planes.id'))
    planes = relationship("Planes")
    airports = relationship("Airports")

    def __init__(self, f_id, departure, arrival, flight_time, airport, plane):
        self.f_id = f_id
        self.departure = departure
        self.arrival = arrival
        self.flight_time = flight_time
        self.airport_id = airport
        self.plane_id = plane

    def __repr__(self):
        return f"{self.departure}, {self.arrival}, {self.flight_time}, {self.airport_id}, {self.plane_id}"


class Planes(Base):
    __tablename__ = 'planes'
    id = Column(Integer, primary_key=True)
    plane = Column(String)

    def __init__(self, plane):
        self.plane = plane

    def __repr__(self):
        return self.plane


class Airports(Base):
    __tablename__ = 'airports'
    id = Column(Integer, primary_key=True)
    airport = Column(String)

    def __init__(self, airport):
        self.airport = airport

    def __repr__(self):
        return self.airport


Base.metadata.create_all(engine)


class Flightsdb():
    def get(self, get_filter=None):
        q = select([Flights.departure, Flights.arrival, Flights.flight_time,
                    Airports.airport, Planes.plane, Flights.f_id]) \
            .where(Flights.airport_id == Airports.id).where(
            Flights.plane_id == Planes.id)
        if get_filter is None:
            dct = [{
                'id': i[5],
                'departure': i[0],
                'arrival': i[1],
                'flight_time': i[2],
                'airport': i[3],
                'plane': i[4]
            } for i in session.execute(q)]
            return sorted(dct, key=lambda x: x['id'])
        else:
            for key in ['id', 'departure', 'arrival', 'flight_time', 'airport',
                        'plane']:
                if get_filter.get(key) is None:
                    get_filter[key] = "%"
            print(get_filter)
            q = q.where(Flights.f_id.like(get_filter['id'])) \
                .where(Flights.departure.like(get_filter['departure'])) \
                .where(Flights.arrival.like(get_filter['arrival'])) \
                .where(Flights.flight_time.like(get_filter['flight_time'])) \
                .where(Airports.airport.like(get_filter['airport'])) \
                .where(Planes.plane.like(get_filter['plane']))
            dct = [{
                'id': i[5],
                'departure': i[0],
                'arrival': i[1],
                'flight_time': i[2],
                'airport': i[3],
                'plane': i[4]
            } for i in session.execute(q)]
            return dct

    def append(self, item):  # correct data
        if item['id'] in [i[0] for i in
                          session.execute(select([Flights.f_id]))]:
            return 1
        else:
            session.add(Airports(item['airport']))
            session.add(Planes(item['plane']))
            real_id = session.query(Airports.id)[-1][0] + 1
            session.add(Flights(item['id'], item['departure'], item['arrival'],
                                item['flight_time'], real_id, real_id))
            session.commit()

    def pop(self, _id):  # correct id
        flight = session.query(Flights).filter_by(f_id=_id)[:]
        if len(flight) == 0:
            return 1
        print(type(flight))
        flight = flight[0]
        session.delete(session.query(Airports).get(flight.airport_id))
        session.delete(session.query(Planes).get(flight.plane_id))
        session.delete(flight)
        session.commit()
        return 0

    def update(self, item):  # correct item
        flight = session.query(Flights).filter_by(f_id=item.get('id'))[:]
        if len(flight) == 0:
            return 1
        cur_id = item.pop('id')
        flight = flight[0]
        if item.get('airport') is not None:
            session.query(Airports).filter(
                Airports.id == flight.airport_id).update(
                {'airport': item['airport']})
            item.pop('airport')
        if item.get('plane') is not None:
            session.query(Planes).filter(Planes.id == flight.plane_id).update(
                {'plane': item['plane']})
            item.pop('plane')
        session.query(Flights).filter(Flights.f_id == cur_id).update(item)
        session.commit()
