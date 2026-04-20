from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import models.farm as models
import schemas.farm_schema as schemas
from database import get_db
from routers.auth_router import oauth2_scheme

router = APIRouter(prefix="/farm", tags=["Manajemen Lahan & Sensor"])

# --- CRUD ZONA ---

@router.post("/zones/", response_model=schemas.PlantZone, status_code=201, summary="Tambah Zona Baru")
def create_zone(zone: schemas.PlantZoneCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    db_zone = models.PlantZone(name=zone.name, location=zone.location)
    db.add(db_zone)
    db.commit()
    db.refresh(db_zone)
    return db_zone

@router.get("/zones/", response_model=List[schemas.PlantZone], summary="Lihat Semua Zona")
def read_zones(db: Session = Depends(get_db)):
    return db.query(models.PlantZone).all()

@router.put("/zones/{zone_id}", response_model=schemas.PlantZone, summary="Update Data Zona")
def update_zone(zone_id: int, zone: schemas.PlantZoneCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    db_zone = db.query(models.PlantZone).filter(models.PlantZone.id == zone_id).first()
    if not db_zone:
        raise HTTPException(status_code=404, detail="Zona tidak ditemukan")
    db_zone.name = zone.name
    db_zone.location = zone.location
    db.commit()
    db.refresh(db_zone)
    return db_zone

@router.delete("/zones/{zone_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Hapus Zona")
def delete_zone(zone_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    db_zone = db.query(models.PlantZone).filter(models.PlantZone.id == zone_id).first()
    if not db_zone:
        raise HTTPException(status_code=404, detail="Zona tidak ditemukan")
    db.delete(db_zone)
    db.commit()
    return None

# --- CRUD LOG SENSOR ---

@router.post("/zones/{zone_id}/logs/", response_model=schemas.SensorLog, status_code=201, summary="Tambah Log Sensor ke Zona")
def create_log_for_zone(zone_id: int, log: schemas.SensorLogCreate, db: Session = Depends(get_db)):
    db_zone = db.query(models.PlantZone).filter(models.PlantZone.id == zone_id).first()
    if not db_zone:
        raise HTTPException(status_code=404, detail="Zona tidak ditemukan!")
    db_log = models.SensorLog(**log.dict(), zone_id=zone_id)
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

@router.delete("/logs/{log_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Hapus Log Sensor")
def delete_log(log_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    db_log = db.query(models.SensorLog).filter(models.SensorLog.id == log_id).first()
    if not db_log:
        raise HTTPException(status_code=404, detail="Log tidak ditemukan")
    db.delete(db_log)
    db.commit()
    return None