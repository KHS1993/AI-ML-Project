from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from database.connection import SessionLocal, get_db

app = FastAPI()

@app.get("/health")
async def health_Check():
    return {"status": "Running"}

@app.get("/test-db")
def test_database(db: Session = Depends(get_db)):
    return {"message": "Database connected!"}

@app.get("/test-table")
def get_table(db: Session = Depends(get_db)):
    query = text("SELECT * FROM test")

    result = db.execute(query)

    table = [dict(row._mapping) for row in result]

    return table

