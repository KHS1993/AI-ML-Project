import pandas as pd

from src.model_config import FEATURE_COLUMNS
from src.model_service import load_model, predict_energy


# Läs en riktig observation från datasetet
df = pd.read_csv("data/energydata_complete.csv")

df["date"] = pd.to_datetime(df["date"])

# Skapa samma tidsfeatures som modellen tränades med
df["hour"] = df["date"].dt.hour
df["day_of_week"] = df["date"].dt.dayofweek
df["is_weekend"] = df["day_of_week"].isin([5, 6]).astype(int)

# Ta en observation och skapa input i exakt rätt format
sample = df.iloc[0]

feature_values = {
    feature: sample[feature]
    for feature in FEATURE_COLUMNS
}

# Ladda modellen från .joblib
model = load_model()

# Gör prediction utan att träna modellen
prediction = predict_energy(
    model,
    feature_values,
)

print("Saved model loaded successfully")
print("Features used:", FEATURE_COLUMNS)
print(f"Prediction: {prediction:.2f} Wh")