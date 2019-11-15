from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()
LogBase = declarative_base()


class Airports(Base):
    __tablename__ = 'airports'

    id = Column(Integer, primary_key=True)
    airport = Column(String, unique=True)


class Airplanes(Base):
    __tablename__ = 'airplanes'

    id = Column(Integer, primary_key=True)
    airplane = Column(String, unique=True)


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String)
    password_hash = Column(String)


class Flights(Base):
    __tablename__ = 'flights'

    id = Column(Integer, primary_key=True)
    plane_id = Column(Integer, ForeignKey('airplanes.id'))
    airport_id = Column(Integer, ForeignKey('airports.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    dep_time = Column(DateTime)
    arr_time = Column(DateTime)
    flight_time = Column(String)
    airport = relationship("Airports", back_populates="flights")
    airplane = relationship("Airplanes", back_populates="flights")
    user = relationship('Users', back_populates='flights')


    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'dep_time': self.dep_time,
            'arr_time': self.arr_time,
            'airplane': self.airplane.airplane,
            'airport': self.airport.airport,
            'flight_time': self.flight_time,
            'user': self.user,
        }


class Log(LogBase):
    __tablename__ = 'log'

    time = Column(DateTime, primary_key=True)
    lavel_name = Column(String)
    name = Column(String)
    remote_addr = Column(String)
    method = Column(String, index=True)
    scheme = Column(String)
    full_path = Column(String)
    json = Column(String)
    status = Column(String)
    resp_time = Column(Float)

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'time': self.time,
            'lavel_name': self.lavel_name,
            'name': self.name,
            'remote_addr': self.remote_addr,
            'method': self.method,
            'scheme': self.scheme,
            'full_path': self.full_path,
            'json': str(self.json),
            'status': self.status,
            'resp_time': self.resp_time,
        }


Airplanes.flights = relationship("Flights", order_by=Flights.id, back_populates='airplane')
Airports.flights = relationship("Flights", order_by=Flights.id, back_populates='airport')
Users.flights = relationship("Flights", order_by=Flights.id, back_populates='user')
