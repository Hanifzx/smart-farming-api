from routers.auth_router import oauth2_scheme
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models.farm as models
import schemas.farm_schema as schemas
from database import get_db

router = APIRouter(prefix="/farm", tags=["Smart Farming Operations"])

# --- ENDPOINT UNTUK ZONA ---

@router.post("/zones/", response_model=schemas.PlantZone, status_code=201)
def create_zone(
    zone: schemas.PlantZoneCreate, 
    db: Session = Depends(get_db), 
    token: str = Depends(oauth2_scheme)
):
    db_zone = models.PlantZone(name=zone.name, location=zone.location)
    db.add(db_zone)
    db.commit()
    db.refresh(db_zone)
    return db_zone

@router.get("/zones/", response_model=List[schemas.PlantZone])
def read_zones(db: Session = Depends(get_db)):
    return db.query(models.PlantZone).all()

# --- ENDPOINT UNTUK LOG SENSOR ---

@router.post("/zones/{zone_id}/logs/", response_model=schemas.SensorLog, status_code=201)
def create_log_for_zone(zone_id: int, log: schemas.SensorLogCreate, db: Session = Depends(get_db)):
    db_zone = db.query(models.PlantZone).filter(models.PlantZone.id == zone_id).first()
    if not db_zone:
        raise HTTPException(status_code=404, detail="Zona tidak ditemukan!")
    
    db_log = models.SensorLog(**log.dict(), zone_id=zone_id)
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log