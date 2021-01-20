from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.types import DateTime, Integer, String, Float
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey, inspect
from flask_restful import Resource
import datetime
from sqlalchemy.sql.schema import Column, Table
from sqlalchemy.types import TIMESTAMP


db = SQLAlchemy()


class Base(db.Model):
    __abstract__ = True

    def toDict(self):
        obj_dict = {}
        for c in inspect(self).mapper.column_attrs:
            value = getattr(self, c.key)
            if value and isinstance(value, datetime.datetime):
                new_value = value.strftime("%Y-%m-%d %H:%M:%S")
                obj_dict[c.key] = new_value
            else:
                obj_dict[c.key] = value
        return obj_dict


station_trips = Table('station_trips', Base.metadata,
                      Column('station_id', ForeignKey(
                          'stations.id'), primary_key=True),
                      Column('trip_id', ForeignKey(
                          'trips.id'), primary_key=True)
                      )


class Station(Base):
    __tablename__ = 'stations'
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(50), nullable=False)
    location = db.Column(String(32), nullable=True)
    date_created = db.Column(TIMESTAMP, default=datetime.datetime.now())
    last_updated = db.Column(TIMESTAMP, onupdate=datetime.datetime.now())
    trips = relationship('Trip',
                         secondary=station_trips,
                         back_populates='stations')

    def __rep__(self):
        return "<Station(name='%')>" % self.name


class Bus(Base):
    __tablename__ = 'buses'
    id = db.Column(Integer, primary_key=True)
    code = db.Column(String(50), nullable=False)
    carrier = db.Column(String(50), nullable=False)
    date_created = db.Column(TIMESTAMP, default=datetime.datetime.now)
    last_updated = db.Column(TIMESTAMP, onupdate=datetime.datetime.now)
    longitude = db.Column(Float(), nullable=True)
    latitude = db.Column(Float(), nullable=True)
    trips = db.relationship("Trip", back_populates='buses', lazy="dynamic")

    def __rep__(self):
        return "<Bus(code='%' carrier='%)>" % self.code, self.carrier


class Trip(Base):
    __tablename__ = 'trips'
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(50), nullable=False)
    dest_station = db.Column(String(50), nullable=False)
    orig_station = db.Column(String(50), nullable=False)
    time = db.Column(TIMESTAMP, nullable=True)
    plateform = db.Column(String(50), nullable=True)
    status = db.Column(Integer, default=0)
    date_created = db.Column(TIMESTAMP, default=datetime.datetime.now)
    last_updated = db.Column(TIMESTAMP, onupdate=datetime.datetime.now)
    bus = db.Column(Integer, ForeignKey('buses.id'))
    buses = db.relationship("Bus", uselist=False, back_populates="trips")
    stations = relationship('Station',
                            secondary=station_trips,
                            back_populates='trips')

    def __rep__(self):
        return "<Trip(name='%' time='%' status='%)>" % self.name, self.time, self.status


def init_db():
    global db
    db.drop_all()
    db.create_all()

    for i in range(1, 11):
        station = Station(name="station {}".format(i))
        db.session.add(station)

    bus = Bus(code="B1452", carrier="TTC",
              latitude=21.654888, longitude=78.489664)
    db.session.add(bus)
    db.session.commit()

    for i in range(1, 11):
        trip = Trip(name="trip {}".format(
            i), dest_station=" London station {} ".format(i), time=datetime.datetime.now(), orig_station="MTL", bus=bus.id, plateform="P{}".format(i))
        db.session.add(trip)

    db.session.commit()
    station = Station.query.filter_by(id=1).first()
    for trip in Trip.query.all():
        station.trips.append(trip)

    db.session.add(station)
    db.session.commit()

    print(" A station with trips")
    print(station.toDict())
    for trip in station.trips:
        print(trip.toDict())

    print("A bus with trips")

    print(bus.toDict())
    for trip in bus.trips:
        print(trip.toDict())

    if __name__ == '__main__':
        init_db()
