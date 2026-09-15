from fastapi import FastAPI, Depends

app = FastAPI()

@app.get("/health")
async def health_Check():
    return {"status": "Running"}

@app.get("test-db")
def test_database(db: Session = Depends(get_db)):
    return {"message": "Database connected!"}