from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.types import DateTime, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from flask_restful import Resource
import datetime


db = SQLAlchemy()
ma = Marshmallow()


class Station(db.Model):
    __tablename__ = 'stations'
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(50), nullable=False)
    location = db.Column(String(32), nullable=True)
    date_created = db.Column(DateTime, default=datetime.datetime.now)

    def __rep__(self):
        return "<Station(name='%')>" % self.name


class Bus(db.Model):
    __tablename__ = 'buses'
    id = db.Column(Integer, primary_key=True)
    code = db.Column(String(50), nullable=False)
    carrier = db.Column(String(50), nullable=False)
    date_created = db.Column(DateTime, default=datetime.datetime.now)
    trips = db.relationship("Trip", backref='bus')

    def __rep__(self):
        return "<Bus(code='%' carrier='%)>" % self.code, self.carrier


class Trip(db.Model):
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


class StationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Station

    id = ma.auto_field()
    name = ma.auto_field()


class BusSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Bus
        
    id = ma.auto_field()
    code = ma.auto_field()
    carrier = ma.auto_field()
    trips = ma.auto_field()


class TripSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Trip
        include_fk = True

    id = ma.auto_field()
    name = ma.auto_field()
    dest = ma.auto_field()
    plateform = ma.auto_field()
    status = ma.auto_field()
    # bus = ma.HyperlinkRelated("bus_detail")


def init_db():
    global db 
    db.drop_all()
    db.create_all()
  
    station = Station(name="test station")
    db.session.add(station)
    db.session.commit()
    print("adding station")

    db.session.commit()

    if __name__ == '__main__':
        init_db()