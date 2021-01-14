from flask_restful import Resource
from app.model import BusSchema, StationSchema, TripSchema, Station, Trip


stations_Schema = StationSchema(many=True)
station_Schema = StationSchema()



class StationResource(Resource):
    
    def get(self, station_id):
        
        station = Station.query.filter_by(id=station_id)
        station = station_Schema.dump(station)
        return {'data': station}, 200

    def delete(self, station_id):
        return '', 204

    def put(self, station_id):
        STATIONS[station_id] = ""
        return station_id, 201


class StationsResource(Resource):

    def get(self):
        stations = Station.query.all()
        stations = stations_Schema.dump(stations)
        return {'data': stations}, 200

    def post(self):
        return '', 200