from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional


class SensorLogBase(BaseModel):
    temperature: float = Field(..., ge=-50, le=60, description="Suhu dalam Celsius (-50 s/d 60)")
    humidity: float = Field(..., ge=0, le=100, description="Kelembapan dalam persen (0 s/d 100)")


class SensorLogCreate(SensorLogBase):
    pass


class SensorLogUpdate(SensorLogBase):
    pass


class SensorLog(SensorLogBase):
    id: int
    timestamp: datetime
    zone_id: int

    class Config:
        orm_mode = True


class PlantZoneBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Nama zona tanaman")
    location: str = Field(..., min_length=1, max_length=200, description="Lokasi zona")


class PlantZoneCreate(PlantZoneBase):
    pass


class PlantZoneUpdate(PlantZoneBase):
    pass


class PlantZone(PlantZoneBase):
    id: int
    logs: List[SensorLog] = []

    class Config:
        orm_mode = True