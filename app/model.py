from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.schema import Column
from sqlalchemy.types import DateTime, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from flask_restful import Resource
import datetime



db = SQLAlchemy()
ma = Marshmallow()


class Station(db.Model):
    __tablename_ = 'stations'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    location = Column(String(32), nullable=True)
    date_created = Column(DateTime, default=datetime.datetime.now)

    def __rep__(self):
        return "<Station(name='%')>" % self.name


class Trip(db.Model, ):
    __tablename = 'trips'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    dest = Column(String(50), nullable=False)
    orig = Column(String(50), nullable=True)
    time = Column(DateTime, nullable=True)
    plateform = db.Column(String(50), nullable=True)
    status = Column(Integer, default=0)
    date_created = Column(DateTime, default=datetime.datetime.now)
    last_updated = Column(DateTime, onupdate=datetime.datetime.now)
    bus_id = Column(Integer, ForeignKey('buses.id'))
    bus = relationship("Bus", back_populates="trips")

    def __rep__(self):
        return "<Trip(name='%' time='%' status='%)>" % self.name, self.time, self.status


class Bus(db.Model):
    __tablename = 'buses'
    id = Column(Integer, primary_key=True)
    code = Column(String(50), nullable=False)
    carrier = Column(String(50), nullable=False)
    date_created = Column(DateTime, default=datetime.datetime.now)

    def __rep__(self):
        return "<Bus(code='%' carrier='%)>" % self.code, self.carrier


class StationSchema(ma.Schema):
    class Meta:
        model = Station

    id = ma.auto_field()
    name = ma.auto_field()


class BusSchema(ma.Schema):
    class Meta:
        model = Bus

    id = ma.auto_field()
    name = ma.auto_field()
    carrier = ma.auto_field()


class TripSchema(ma.Schema):
    class Meta:
        model = Trip

    id = ma.auto_field()
    name = ma.auto_field()
    dest = ma.auto_field()
    plateform = ma.auto_field()
    status = ma.auto_field()
    bus = ma.HyperlinkRelated("bus_detail")