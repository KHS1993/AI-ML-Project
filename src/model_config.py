from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

MODEL_PATH = PROJECT_ROOT / "models" / "decision_tree_model.joblib"

FEATURE_COLUMNS = [
    "T1",
    "RH_1",
    "T2",
    "RH_2",
    "T_out",
    "RH_out",
    "hour",
    "day_of_week",
    "is_weekend",
]

FEATURE_UNITS = {
    "T1": "°C",
    "RH_1": "%",
    "T2": "°C",
    "RH_2": "%",
    "T_out": "°C",
    "RH_out": "%",
    "hour": "0-23",
    "day_of_week": "0-6 (Monday-Sunday)",
    "is_weekend": "0 or 1",
}