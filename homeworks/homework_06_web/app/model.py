from sqlalchemy import ForeignKey, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class Airports(Base):
    __tablename__ = 'airports'

    id = Column(Integer, primary_key=True)
    airport = Column(String, unique=True)


class Airplanes(Base):
    __tablename__ = 'airplanes'

    id = Column(Integer, primary_key=True)
    airplane = Column(String, unique=True)


class Flights(Base):
    __tablename__ = 'flights'

    id = Column(Integer, primary_key=True)
    plane_id = Column(Integer, ForeignKey('airplanes.id'))
    airport_id = Column(Integer, ForeignKey('airports.id'))
    dep_time = Column(DateTime)
    arr_time = Column(DateTime)
    flight_time = Column(String)
    airport = relationship("Airports", back_populates="flights")
    airplane = relationship("Airplanes", back_populates="flights")

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'dep_time': self.dep_time,
            'arr_time': self.arr_time,
            'airplane': self.airplane.airplane,
            'airport': self.airport.airport,
            'flight_time': self.flight_time,
        }


Airplanes.flights = relationship("Flights", order_by=Flights.id, back_populates='airplane')
Airports.flights = relationship("Flights", order_by=Flights.id, back_populates='airport')
