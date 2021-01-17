from flask_restful import Resource, request
from flask import jsonify, make_response
from app.model import Trip, db, Bus
import json


class TripResource(Resource):

    def get(self, trip_id):

        trip = Trip.query.filter_by(id=trip_id).first()
        if not trip:
            return "", 200
        return jsonify(trip.toDict())

    def delete(self, trip_id):
        trip = Trip.query.filter_by(id=trip_id).first()
        if not trip:
            Trip.query.delete(trip)

        return {'id': trip.id}, 204

    def post(self, trip_id):
        body = request.get_json()

        if not body:
            return {'message': 'invalid data '}, 422

        if "id" in body.keys():
            del body['id']

        _ok = Trip.query.filter_by(id=trip_id).update(
            {**body}, synchronize_session=False)
        db.session.commit()

        if not _ok:
            return {'message': 'Trip already exists'}, 400

        return jsonify({'id': trip_id})


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
        if not data:
            return {'message': 'No input data found'}, 400

        _trip = Trip.query.filter_by(name=data['name']).first()

        if _trip:
            return {'message': 'Trip name already exists'}, 400

        if "id" in data.keys():
            del data['id']

        _trip = Trip(**data)

        db.session.add(_trip)
        db.session.commit()
        return jsonify(_trip.toDict())
