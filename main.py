from fastapi import FastAPI
import models.farm as farm_models
import models.user as user_models
from database import engine
from routers import farm_router, auth_router

app = FastAPI(
    title="Smart Farming API",
    description="API untuk monitoring kelembapan dan nutrisi tanaman berbasis zona.",
    version="1.0.0"
)

farm_models.Base.metadata.create_all(bind=engine)
user_models.Base.metadata.create_all(bind=engine)

app.include_router(auth_router.router)
app.include_router(farm_router.router)