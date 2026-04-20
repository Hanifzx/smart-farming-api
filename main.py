from fastapi import FastAPI
import models.farm as models
from database import engine
from routers import farm_router, auth_router

app = FastAPI(
    title="Smart Farming API",
    description="API untuk monitoring kelembapan dan nutrisi tanaman berbasis zona.",
    version="1.0.0"
)

models.Base.metadata.create_all(bind=engine)

app.include_router(auth_router.router)
app.include_router(farm_router.router)