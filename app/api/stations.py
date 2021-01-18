from flask_restful import Resource, reqparse, request
from flask import jsonify, make_response
from app.model import Bus, Station, Trip, db
import json


class StationResource(Resource):

    def get(self, station_id):

        station = Station.query.filter(Station.id == station_id).first()
        if not station:
            return "", 200
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

        if "id" in body.keys():
            del body['id']

        _ok = Station.query.filter_by(id=station_id).update(
            {**body}, synchronize_session=False)
        db.session.commit()

        if not _ok:
            return {'message': 'station already exists'}, 400

        return jsonify({'id': station_id})


class StationTripResource(Resource):

    def get(self, station_id):
        parser = reqparse.RequestParser()
        parser.add_argument('interval', type=int, required=False,
                            help='interval cannot be converted')
        args = parser.parse_args()
        if args['interval']:
            print("interval {}".format(args['interval']))

        station = Station.query.filter(Station.id == station_id).first()
        if not station or not station.trips:
            return {}, 200
        else:
            tripArr = []
            _trip = {}
            for trip in station.trips:
                if trip.bus:
                    _bus = Bus.query.filter_by(id=trip.bus).first()
                    if _bus:
                        _trip = trip.toDict()
                        _trip['bus'] = _bus.toDict()
                tripArr.append(_trip)

        return jsonify(tripArr)


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

        _station = Station.query.filter_by(name=data['name']).first()

        if _station:
            return {'message': 'station name already exists'}, 400

        if "id" in data.keys():
            del data['id']

        _station = Station(**data)

        db.session.add(_station)
        db.session.commit()
        return jsonify(_station.toDict())
