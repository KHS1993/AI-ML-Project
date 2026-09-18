import joblib
import pandas as pd

from src.model_config import FEATURE_COLUMNS, MODEL_PATH


def load_model():
    """Load the already trained model from disk."""
    return joblib.load(MODEL_PATH)


def predict_energy(model, feature_values):
    """
    Predict appliance energy use from one set of feature values.

    feature_values must contain all features defined in FEATURE_COLUMNS.
    """
    input_data = pd.DataFrame(
        [feature_values],
        columns=FEATURE_COLUMNS,
    )

    prediction = model.predict(input_data)

    return float(prediction[0])