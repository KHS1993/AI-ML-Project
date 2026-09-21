from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends

from sqlalchemy import text
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database.connection import SessionLocal, get_db
from database.load_csv import load_users_from_csv

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting Backend.")

    db = SessionLocal()

    try:
        load_users_from_csv(db)
    finally:
        db.close()

    print("Database Loaded.")

    yield
    print("Apllication Stopped.")

app = FastAPI()

@app.get("/health")
async def health_Check():
    return {"status": "Running"}

@app.get("/test-db")
def test_database(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"message": "Database connected!"}

@app.get("/test-table")
def get_table(db: Session = Depends(get_db)):
    query = text("SELECT COUNT(*) FROM test")

    result = db.execute(query)

##    table = [dict(row._mapping) for row in result]


    return {"rows": result.scalar()}

# --- Pydantic-modell och Predict-endpoint för Streamlit ---
#Tar emot inmatade mätvärden från frontend (ui.py) via POST och returnerar en prediktion
class EnergyInput(BaseModel):
    T1: float
    RH_1: float
    T2: float
    RH_2: float
    Windspeed: float
    Visibility: float

@app.post("/predict")
def predict_energy(data: EnergyInput):
    # Här kopplar du in din tränade maskininlärningsmodell sen
    predicted_value = 145.50  
    return {"prediction": predicted_value}
