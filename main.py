from fastapi import FastAPI
import models.farm as models
from database import engine
from routers import farm_router 

app = FastAPI(title="Smart Farming API")

models.Base.metadata.create_all(bind=engine)

app.include_router(farm_router.router)

@app.get("/")
def root():
    return {"message": "Smart Farming API is Running"}