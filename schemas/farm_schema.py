from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class SensorLogBase(BaseModel):
    temperature: float
    humidity: float

class SensorLogCreate(SensorLogBase):
    pass

class SensorLog(SensorLogBase):
    id: int
    timestamp: datetime
    zone_id: int
    class Config:
        orm_mode = True

class PlantZoneBase(BaseModel):
    name: str
    location: str

class PlantZoneCreate(PlantZoneBase):
    pass

class PlantZone(PlantZoneBase):
    id: int
    logs: List[SensorLog] = [] 
    class Config:
        orm_mode = True