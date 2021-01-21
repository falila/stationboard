from pydantic import BaseModel
from datetime import datetime


class CreateStationDto(BaseModel):
    name: str
    location: str


class UpdateStationDto(BaseModel):
    id: int
    name: str
    location: str
    date_created: datetime


class CreateTripDto(BaseModel):
    bus: int
    dest_station: str
    name: str
    orig_station: str
    plateform: str = "P14"
    status: int
    time: datetime = None


class UpdateTripDto(BaseModel):
    bus: int
    date_created: datetime
    dest_station: str
    id: int
    name: str
    orig_station: str
    plateform: str = "P14"
    status: int = 0
    time: datetime = None
