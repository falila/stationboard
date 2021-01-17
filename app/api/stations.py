from flask_restful import Resource, request
from flask import jsonify, make_response
from app.model import Station, Trip, db
import json


class StationResource(Resource):
    
    def get(self, station_id):
        
        station = Station.query.filter(Station.id == station_id).first()
        return jsonify(station.toDict())

    def delete(self, station_id):
        station = Station.query.filter_by(id=station_id).first()
        if not station:
            Station.query.delete(station)

        return {'id': station.id}, 204

    def post(self, station_id):
        body = request.get_json()
        
        if not body:
            return {'message': 'invalid data '}, 422

        _ok = Station.query.filter_by(id=station_id).update({**body}, synchronize_session=False)
        db.session.flush()  

        if not _ok:
            return {'message': 'station already exists'}, 400
     
        return jsonify({'id': station_id})


class StationsResource(Resource):

    def get(self):
        stations = Station.query.all()
        statArr = []
        for station in stations:
            statArr.append(station.toDict())

        return jsonify(statArr)

    def post(self):
        
        data = request.get_json(force=True)
        if not data:
            return {'message': 'No input data found'}, 400         

        #data , errors = station_Schema.load(data=data)   
       
        _station = Station.query.filter_by(name=data['name']).first()

        if _station:
            return {'message': 'station name already exists'}, 400
 
        _station = Station(**data)
        print(_station.toDict())

        db.session.add(_station)
        db.session.flush()   
        return jsonify(_station.toDict())
