from flask_restful import Resource, reqparse, request
from flask import jsonify, make_response
from app.model import Bus, Station, Trip, db
import json
from app.api.model_dto import CreateStationDto, UpdateStationDto
from pydantic import ValidationError


class StationResource(Resource):

    def get(self, station_id):

        station = Station.query.filter(Station.id == station_id).first()
        if not station:
            return {'message': 'station not found'}, 400
        return jsonify(station.toDict())

    def delete(self, station_id):
        try:
            Station.query.filter_by(id=station_id).delete(
                synchronize_session=False)
            db.session.commit()
            return {'message': 'succes', 'id': station_id}, 204
        except Exception as e:
            return {'message': str(e)}, 422

    def post(self, station_id):
        body = request.get_json()
        try:
            _updatedStationDto = UpdateStationDto(**body)
            Station.query.filter_by(id=station_id).update(
                {**_updatedStationDto.dict()}, synchronize_session=False)
            db.session.commit()
        except ValidationError as e:
            return e.errors(), 422
        except Exception as e:
            return {'message': 'error'}, 422

        return jsonify({'id': station_id})


class StationTripResource(Resource):

    def get(self, station_id):
        # TODO rewrite this code
        parser = reqparse.RequestParser()
        parser.add_argument('interval', type=int, required=False,
                            help='interval cannot be converted')
        args = parser.parse_args()
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
        stationDto = None
        try:
            stationDto = CreateStationDto(**data)
        except ValidationError as e:
            return e.errors(), 422

        if Station.query.filter_by(name=stationDto.name).count():
            return {'message': 'A station name already exists'}, 422

        _station_to_created = Station(**stationDto.dict())

        db.session.add(_station_to_created)
        db.session.commit()
        _st = _station_to_created.toDict()
        _st['date_created'] = _station_to_created.date_created.strftime(
            "%Y-%m-%d %H:%M:%S")
        return jsonify(_st)
