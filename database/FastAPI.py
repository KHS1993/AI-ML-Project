from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session

from database.connection import get_db
from src.model_service import load_model, predict_energy


# --------------------------------------------------
# 1. Ladda den sparade modellen en gång
# --------------------------------------------------

model = load_model()


# --------------------------------------------------
# 2. Skapa FastAPI-applikationen
# --------------------------------------------------

app = FastAPI()


# --------------------------------------------------
# 3. Inputmodell för prediction
# --------------------------------------------------

class EnergyInput(BaseModel):
    T1: float
    RH_1: float
    T2: float
    RH_2: float
    T_out: float
    RH_out: float
    hour: int
    day_of_week: int
    is_weekend: int


# --------------------------------------------------
# 4. Health check
# --------------------------------------------------

@app.get("/health")
async def health_check():
    return {"status": "Running"}


# --------------------------------------------------
# 5. Testa databasanslutning
# --------------------------------------------------

@app.get("/test-db")
def test_database(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))

    return {
        "message": "Database connected!"
    }


# --------------------------------------------------
# 6. Kontrollera antal rader i databasen
# --------------------------------------------------

@app.get("/test-table")
def get_table(db: Session = Depends(get_db)):
    query = text("SELECT COUNT(*) FROM test")

    result = db.execute(query)

    return {
        "rows": result.scalar()
    }


# --------------------------------------------------
# 7. Prediction-endpoint
# --------------------------------------------------

@app.post("/predict")
def predict_appliances(data: EnergyInput):
    feature_values = data.model_dump()

    prediction = predict_energy(
        model,
        feature_values,
    )

    return {
        "prediction": prediction,
        "unit": "Wh",
    }