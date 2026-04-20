from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import datetime

class PlantZone(Base):
    __tablename__ = "plant_zones"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    location = Column(String)
    
    logs = relationship("SensorLog", back_populates="zone", cascade="all, delete-orphan")

class SensorLog(Base):
    __tablename__ = "sensor_logs"
    id = Column(Integer, primary_key=True, index=True)
    temperature = Column(Float)
    humidity = Column(Float)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    zone_id = Column(Integer, ForeignKey("plant_zones.id"))
    
    zone = relationship("PlantZone", back_populates="logs")