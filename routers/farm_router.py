from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import models.farm as models
import schemas.farm_schema as schemas
from database import get_db
from routers.auth_router import get_current_user

router = APIRouter(prefix="/farm", tags=["Manajemen Lahan & Sensor"])

# ============================================================
#  CRUD ZONA TANAMAN (PlantZone) — Create, Read, Update, Delete
# ============================================================

@router.post(
    "/zones/",
    response_model=schemas.PlantZone,
    status_code=status.HTTP_201_CREATED,
    summary="Tambah Zona Baru",
    description="Membuat zona tanaman baru. Membutuhkan autentikasi JWT."
)
def create_zone(zone: schemas.PlantZoneCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    db_zone = models.PlantZone(name=zone.name, location=zone.location)
    db.add(db_zone)
    db.commit()
    db.refresh(db_zone)
    return db_zone


@router.get(
    "/zones/",
    response_model=List[schemas.PlantZone],
    summary="Lihat Semua Zona",
    description="Mengambil daftar semua zona tanaman beserta log sensor terkait. Membutuhkan autentikasi JWT."
)
def read_zones(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return db.query(models.PlantZone).all()


@router.get(
    "/zones/{zone_id}",
    response_model=schemas.PlantZone,
    summary="Lihat Zona berdasarkan ID",
    description="Mengambil detail satu zona tanaman beserta log sensor terkait berdasarkan ID. Membutuhkan autentikasi JWT."
)
def read_zone(zone_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    db_zone = db.query(models.PlantZone).filter(models.PlantZone.id == zone_id).first()
    if not db_zone:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Zona tidak ditemukan")
    return db_zone


@router.put(
    "/zones/{zone_id}",
    response_model=schemas.PlantZone,
    summary="Update Data Zona",
    description="Mengupdate nama dan lokasi zona tanaman berdasarkan ID. Membutuhkan autentikasi JWT."
)
def update_zone(zone_id: int, zone: schemas.PlantZoneUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    db_zone = db.query(models.PlantZone).filter(models.PlantZone.id == zone_id).first()
    if not db_zone:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Zona tidak ditemukan")
    db_zone.name = zone.name
    db_zone.location = zone.location
    db.commit()
    db.refresh(db_zone)
    return db_zone


@router.delete(
    "/zones/{zone_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Hapus Zona",
    description="Menghapus zona tanaman beserta semua log sensor terkait (cascade delete). Membutuhkan autentikasi JWT."
)
def delete_zone(zone_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    db_zone = db.query(models.PlantZone).filter(models.PlantZone.id == zone_id).first()
    if not db_zone:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Zona tidak ditemukan")
    db.delete(db_zone)
    db.commit()
    return None


# ============================================================
#  CRUD LOG SENSOR (SensorLog) — Create, Read, Update, Delete
# ============================================================

@router.post(
    "/zones/{zone_id}/logs/",
    response_model=schemas.SensorLog,
    status_code=status.HTTP_201_CREATED,
    summary="Tambah Log Sensor ke Zona",
    description="Menambahkan data log sensor (suhu & kelembapan) ke zona tertentu. Membutuhkan autentikasi JWT."
)
def create_log_for_zone(zone_id: int, log: schemas.SensorLogCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    db_zone = db.query(models.PlantZone).filter(models.PlantZone.id == zone_id).first()
    if not db_zone:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Zona tidak ditemukan!")
    db_log = models.SensorLog(**log.dict(), zone_id=zone_id)
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log


@router.get(
    "/zones/{zone_id}/logs/",
    response_model=List[schemas.SensorLog],
    summary="Lihat Semua Log Sensor per Zona",
    description="Mengambil daftar semua log sensor yang tercatat pada zona tertentu. Membutuhkan autentikasi JWT."
)
def read_logs_by_zone(zone_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    db_zone = db.query(models.PlantZone).filter(models.PlantZone.id == zone_id).first()
    if not db_zone:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Zona tidak ditemukan!")
    return db.query(models.SensorLog).filter(models.SensorLog.zone_id == zone_id).all()


@router.get(
    "/logs/{log_id}",
    response_model=schemas.SensorLog,
    summary="Lihat Log Sensor berdasarkan ID",
    description="Mengambil detail satu log sensor berdasarkan ID. Membutuhkan autentikasi JWT."
)
def read_log(log_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    db_log = db.query(models.SensorLog).filter(models.SensorLog.id == log_id).first()
    if not db_log:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Log tidak ditemukan")
    return db_log


@router.put(
    "/logs/{log_id}",
    response_model=schemas.SensorLog,
    summary="Update Log Sensor",
    description="Mengupdate data suhu dan kelembapan pada log sensor berdasarkan ID. Membutuhkan autentikasi JWT."
)
def update_log(log_id: int, log: schemas.SensorLogUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    db_log = db.query(models.SensorLog).filter(models.SensorLog.id == log_id).first()
    if not db_log:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Log tidak ditemukan")
    db_log.temperature = log.temperature
    db_log.humidity = log.humidity
    db.commit()
    db.refresh(db_log)
    return db_log


@router.delete(
    "/logs/{log_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Hapus Log Sensor",
    description="Menghapus satu log sensor berdasarkan ID. Membutuhkan autentikasi JWT."
)
def delete_log(log_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    db_log = db.query(models.SensorLog).filter(models.SensorLog.id == log_id).first()
    if not db_log:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Log tidak ditemukan")
    db.delete(db_log)
    db.commit()
    return None