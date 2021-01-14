from flask_restful import Resource


STATIONS = {
    'stations' : [
        {
        'id':1, 'name':'NORTHBOUND', 'location':'south of the city', 'trips': [
            {'id':1, 'code':'TR01', 'platf':'ptf-56','time':'2:30pm', 'status':'on time', 'dest':'London ON'},
            {'id':2, 'code':'TR02', 'platf':'ptf-25','time':'00:3am', 'status':'on time', 'dest':'Montreal QC'},
            {'id':3, 'code':'TR03', 'platf':'ptf-89','time':'4:30pm', 'status':'on time', 'dest':'Toronto ON'},
         ]
       },
    {},
  ]
}


class Station(Resource):
    
    def get(self, station_id):
        station = None
        for _station in STATIONS['stations']:
            if _station['id'] == station_id:
                station = _station
                break
        return station, 200

    def delete(self, station_id):
        del STATIONS[station_id]
        return '', 204

    def put(self, station_id):
        STATIONS[station_id] = ""
        return station_id, 201


class Stations(Resource):

    def get(self):
        return STATIONS, 200

    def post(self):
        return STATIONS