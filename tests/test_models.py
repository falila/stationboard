from app.model import Bus, Station
import datetime


def test_new_station():
    """
    GIVEN a Station model
    WHEN a new Station is Created
    THEN check the name, location, id,date_cretead are defined as they should. 
    """
    today = datetime.datetime.today()
    station = Station(id=1, name="Toronto Union", location="Dundas and Young",
                      date_created=today,
                      last_updated=today)
    assert station.id == 1
    assert station.name == "Toronto Union"
    assert station.location == "Dundas and Young"
    assert station.date_created == today


def test_new_bus():
    """
    GIVEN a Bus model
    WHEN a new Bus is Created
    THEN check the code, longitude, latitude, id,date_cretead are defined correctly. 
    """
    today = datetime.datetime.now()
    bus = Bus(id=1, code="B0111", carrier="TTC", date_created=today,
              longitude=12.457898, latitude=45.698574,
              )

    assert bus.id == 1
    assert bus.code == "B0111"
    assert bus.carrier == "TTC"
    assert bus.date_created == today
    assert bus.longitude == 12.457898
    assert bus.latitude == 45.698574
