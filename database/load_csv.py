import csv
from pathlib import Path

from sqlalchemy import text
from sqlalchemy.orm import Session
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parents[1]

def load_users_from_csv(db: Session):
    csv_path = PROJECT_ROOT / "data" / "energydata_complete.csv"
    print(csv_path)
    with csv_path.open("r", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))

    try:
        db.execute(text("DELETE FROM test"))

        data = [
            {
                "date": datetime.strptime(row["date"], "%Y-%m-%d %H:%M:%S").date(),
                "Appliances": int(row["Appliances"]),
                "lights": int(row["lights"]),
                "T1": float(row["T1"]),
                "RH_1": float(row["RH_1"]),
                "T2": float(row["T2"]),
                "RH_2": float(row["RH_2"]),
                "T3": float(row["T3"]),
                "RH_3": float(row["RH_3"]),
                "T4": float(row["T4"]),
                "RH_4": float(row["RH_4"]),
                "T5": float(row["T5"]),
                "RH_5": float(row["RH_5"]),
                "T6": float(row["T6"]),
                "RH_6": float(row["RH_6"]),
                "T7": float(row["T7"]),
                "RH_7": float(row["RH_7"]),
                "T8": float(row["T8"]),
                "RH_8": float(row["RH_8"]),
                "T9": float(row["T9"]),
                "RH_9": float(row["RH_9"]),
                "T_out": float(row["T_out"]),
                "Press_mm_hg": float(row["Press_mm_hg"]),
                "RH_out": float(row["RH_out"]),
                "Windspeed": float(row["Windspeed"]),
                "Visibility": float(row["Visibility"]),
                "Tdewpoint": float(row["Tdewpoint"]),
                "rv1": float(row["rv1"]),
                "rv2": float(row["rv2"]),
            }
            for row in rows
        ]

        if data:
            db.execute(
                text("""
                    INSERT INTO test (date, "Appliances", lights, "T1", "RH_1", "T2", "RH_2", "T3", "RH_3", "T4", "RH_4", "T5", "RH_5", "T6", "RH_6", "T7", "RH_7", "T8", "RH_8", "T9", "RH_9", "T_out", "Press_mm_hg", "RH_out", "Windspeed", "Visibility", "Tdewpoint", rv1, rv2)
                    VALUES (:date, :Appliances, :lights, :T1, :RH_1, :T2, :RH_2, :T3, :RH_3, :T4, :RH_4, :T5, :RH_5, :T6, :RH_6, :T7, :RH_7, :T8, :RH_8, :T9, :RH_9, :T_out, :Press_mm_hg, :RH_out, :Windspeed, :Visibility, :Tdewpoint, :rv1, :rv2)
                """),
                data
            )

        db.commit()

        print(f"Imported {len(data)} entires.")

    except Exception:
        db.rollback()
        raise