from flask_restful import Resource, request
from flask import jsonify, make_response
from app.model import Trip, db, Bus
from app.api.model_dto import UpdateTripDto, CreateTripDto
from pydantic import ValidationError

import json


class TripResource(Resource):

    def get(self, trip_id):
        try:
            trip = Trip.query.filter_by(id=trip_id).first()
            if not trip:
                return {'message': 'No trip was found'}, 200
            return trip.toDict(), 200
        except Exception as e:
            return {'message': str(e)}, 422

    def delete(self, trip_id):
        try:
            Trip.query.filter_by(id=trip_id).delete(
                synchronize_session=False)
            db.session.commit()
            return {'message': 'succes', 'id': trip_id}, 204
        except Exception as e:
            return {'message': str(e)}, 422

    def post(self, trip_id):
        body = request.get_json()
        try:
            _tripDto = UpdateTripDto(**body)

            Trip.query.filter_by(id=trip_id).update(
                {**_tripDto.dict()}, synchronize_session=False)
            db.session.commit()
        except ValidationError as e:
            return e.errors, 422
        except Exception as e:
            return {'message': 'error cannot update a trip'}, 400
        return {'id': trip_id}, 200


class TripsResource(Resource):

    def get(self):
        trips = Trip.query.all()
        tripArr = []
        _trip = {}
        for trip in trips:
            if trip.bus:
                _bus = Bus.query.filter_by(id=trip.bus).first()
                if _bus:
                    _trip = trip.toDict()
                    _trip['bus'] = _bus.toDict()
            tripArr.append(_trip)

        return jsonify(tripArr)

    def post(self):
        data = request.get_json(force=True)
        _trip = None
        try:
            _trip = CreateTripDto(**data)
        except ValidationError as e:
            return e.errors(), 422

        if Trip.query.filter_by(name=_trip.name).count():
            return {'message': 'A trip already exists with the same name.'}, 422
        _trip_to_save = Trip(**_trip.dict())
        db.session.add(_trip_to_save)
        db.session.commit()
        return jsonify(_trip_to_save.toDict())
