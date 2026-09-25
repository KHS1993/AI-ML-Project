# Saved Model Usage

## Model

The selected model is a Decision Tree Regressor:

`DecisionTreeRegressor(max_depth=7, random_state=42)`

The trained model is saved as:

`models/decision_tree_model.joblib`

The model can be loaded and used for prediction without retraining.

---

## Expected features

The model expects the following nine features in this order:

| Feature | Description | Unit / format |
|---|---|---|
| `T1` | Indoor temperature | °C |
| `RH_1` | Indoor relative humidity | % |
| `T2` | Indoor temperature | °C |
| `RH_2` | Indoor relative humidity | % |
| `T_out` | Outdoor temperature | °C |
| `RH_out` | Outdoor relative humidity | % |
| `hour` | Hour of day | 0–23 |
| `day_of_week` | Day of week | 0–6, Monday = 0 |
| `is_weekend` | Weekend indicator | 0 or 1 |

The target predicted by the model is `Appliances`, measured in Wh.

The dataset contains measurements at 10-minute intervals.

---

## Feature order

The model expects the features in the following order:

```python
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
```

The same feature order is defined in:

`src/model_config.py`

This allows the training code and the FastAPI backend to use the same model input structure.

---

## Loading the model

The model is loaded from disk using `joblib`.

The reusable loading logic is located in:

`src/model_service.py`

Example:

```python
from src.model_service import load_model

model = load_model()
```

No `.fit()` call is required when the saved model is used.

The model has already been trained before it is saved.

In the application, the FastAPI backend loads the saved model and reuses it for prediction requests.

---

## Making a prediction

Predictions are made through the `predict_energy()` function in:

`src/model_service.py`

Example:

```python
from src.model_service import load_model, predict_energy

model = load_model()

feature_values = {
    "T1": 20.0,
    "RH_1": 40.0,
    "T2": 19.5,
    "RH_2": 42.0,
    "T_out": 8.0,
    "RH_out": 75.0,
    "hour": 14,
    "day_of_week": 2,
    "is_weekend": 0,
}

prediction = predict_energy(
    model,
    feature_values,
)

print(prediction)
```

The returned value is the estimated appliance energy use in Wh.

In the complete application, this prediction function is called by the FastAPI `/predict` endpoint.

---

## Time-based features

Three of the model features are created from the original `date` column:

- `hour`
- `day_of_week`
- `is_weekend`

During training they are created using:

```python
df["hour"] = df["date"].dt.hour

df["day_of_week"] = df["date"].dt.dayofweek

df["is_weekend"] = (
    df["day_of_week"]
    .isin([5, 6])
    .astype(int)
)
```

In the Streamlit application, the user selects a date and time.

Streamlit converts the selected date and time into:

- `hour`
- `day_of_week`
- `is_weekend`

These values are then sent together with the other required features to the FastAPI `/predict` endpoint.

The FastAPI backend validates the input before passing the feature values to the saved model.

---

## Saved model verification

The training script saves the selected model using `joblib`.

The model is then loaded again and predictions from the original model and the loaded model are compared.

The verification produced:

```text
Loaded model predictions match: True
```

This confirms that saving and loading the model does not change its predictions.

---

## Independent model loading test

The saved model was also tested from a separate Python script:

`verify_saved_model.py`

This script loads the model directly from:

`models/decision_tree_model.joblib`

without running the training process again.

The verification produced:

```text
Saved model loaded successfully
Features used: ['T1', 'RH_1', 'T2', 'RH_2', 'T_out', 'RH_out', 'hour', 'day_of_week', 'is_weekend']
Prediction: 121.52 Wh
```

This demonstrates that the saved model can be loaded and used independently from `train.py`.

---

## Application integration

The saved model is used through the FastAPI backend.

The Streamlit application does not load or train the model directly.

Instead, Streamlit collects the user's input and sends it to the FastAPI `/predict` endpoint using an HTTP POST request.

The prediction flow is:

```text
User
    ↓
Streamlit
    ↓
POST /predict
    ↓
FastAPI
    ↓
src/model_service.py
    ↓
models/decision_tree_model.joblib
    ↓
Prediction
    ↓
FastAPI response
    ↓
Streamlit
```

FastAPI loads the saved model using:

```python
from src.model_service import load_model, predict_energy

model = load_model()
```

When a prediction request is received, FastAPI sends the validated feature values to:

```python
prediction = predict_energy(
    model,
    feature_values,
)
```

The prediction is returned from FastAPI as JSON and displayed in Streamlit.

The model is not retrained when the application starts or when a prediction is requested.

---

## Files used for model reuse

The saved-model workflow currently uses:

```text
models/
└── decision_tree_model.joblib

src/
├── model_config.py
└── model_service.py

database/
└── FastAPI.py

app.py
verify_saved_model.py
train.py
```

### `model_config.py`

Contains:

- model path
- expected feature names
- feature order
- feature units

### `model_service.py`

Contains reusable functions for:

- loading the saved model
- validating required model features
- creating model input
- making predictions

### `FastAPI.py`

Contains the backend API.

It:

- loads the saved model
- validates prediction input with Pydantic
- exposes the `/predict` endpoint
- calls `predict_energy()`
- returns the prediction to the frontend

### `app.py`

Contains the Streamlit frontend.

It:

- collects user input
- creates the time-based features
- sends input to FastAPI
- receives the prediction
- displays the predicted energy consumption

### `verify_saved_model.py`

Checks that the saved model can be loaded and used without retraining.

### `train.py`

Trains the selected model, saves it and verifies that predictions remain identical after loading.

---

## Summary

The selected Decision Tree model is saved as a `.joblib` file and can be reused without retraining.

The following requirements have been verified:

- The selected model is saved to disk.
- The saved model can be loaded again.
- Predictions before and after saving/loading are identical.
- The model can make predictions from a separate script without retraining.
- The required features and their units are documented.
- The feature order is shared through `model_config.py`.
- FastAPI loads and uses the saved model through `model_service.py`.
- Streamlit sends user input to the FastAPI `/predict` endpoint.
- The model is not retrained for every prediction.

The complete application flow is:

```text
Streamlit → FastAPI → model_service → saved model → prediction → FastAPI → Streamlit
```

This means the saved model can be reused by the FastAPI backend without retraining, while Streamlit acts as the user interface for making prediction requests.