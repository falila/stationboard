from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.types import DateTime, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey, inspect
from flask_restful import Resource
import datetime


db = SQLAlchemy()


class Base(db.Model):
    __abstract__ = True

    def toDict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}


class Station(Base):
    __tablename__ = 'stations'
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(50), nullable=False)
    location = db.Column(String(32), nullable=True)
    date_created = db.Column(DateTime, default=datetime.datetime.now)
    last_updated = db.Column(DateTime, onupdate=datetime.datetime.now)

    def __rep__(self):
        return "<Station(name='%')>" % self.name


class Bus(Base):
    __tablename__ = 'buses'
    id = db.Column(Integer, primary_key=True)
    code = db.Column(String(50), nullable=False)
    carrier = db.Column(String(50), nullable=False)
    date_created = db.Column(DateTime, default=datetime.datetime.now)
    last_updated = db.Column(DateTime, onupdate=datetime.datetime.now)
    trips = db.relationship("Trip", backref='bus')

    def __rep__(self):
        return "<Bus(code='%' carrier='%)>" % self.code, self.carrier

    def toDict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}


class Trip(Base):
    __tablename__ = 'trips'
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(50), nullable=False)
    dest = db.Column(String(50), nullable=False)
    orig = db.Column(String(50), nullable=True)
    time = db.Column(DateTime, nullable=True)
    plateform = db.Column(String(50), nullable=True)
    status = db.Column(Integer, default=0)
    date_created = db.Column(DateTime, default=datetime.datetime.now)
    last_updated = db.Column(DateTime, onupdate=datetime.datetime.now)
    bus_id = db.Column(Integer, ForeignKey('buses.id'))
    #bus = db.relationship("Bus", back_populates="trips", )

    def __rep__(self):
        return "<Trip(name='%' time='%' status='%)>" % self.name, self.time, self.status

    def toDict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}


def init_db():
    global db
    db.drop_all()
    db.create_all()

    for i in range(10):
        station = Station(name="station {}".format(i))
        db.session.add(station)

    db.session.commit()

    if __name__ == '__main__':
        init_db()
