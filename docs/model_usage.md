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

This allows both the training code and the Streamlit application to use the same model input structure.

---

## Loading the model

The model is loaded from disk using `joblib`.

```python
from src.model_service import load_model

model = load_model()
```

No `.fit()` call is required when the saved model is used.

The model has already been trained before it is saved.

---

## Making a prediction

Predictions are made through the `predict_energy()` function.

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

---

## Time-based features

Three of the model features are created from the original `date` column:

- `hour`
- `day_of_week`
- `is_weekend`

They are created using:

```python
df["hour"] = df["date"].dt.hour

df["day_of_week"] = df["date"].dt.dayofweek

df["is_weekend"] = (
    df["day_of_week"]
    .isin([5, 6])
    .astype(int)
)
```

The Streamlit application must provide these features in the same format used during model training.

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

## Streamlit integration

The Streamlit application should use the saved model instead of training a new model when the application starts.

The intended flow is:

```text
Streamlit
    ↓
src/model_service.py
    ↓
models/decision_tree_model.joblib
    ↓
prediction
```

Streamlit should therefore load the model using:

```python
from src.model_service import load_model, predict_energy

model = load_model()
```

and then use:

```python
prediction = predict_energy(
    model,
    feature_values,
)
```

The Streamlit application should not call:

```python
model.fit(...)
```

because the model has already been trained and saved.

---

## Files used for model reuse

The saved-model workflow currently uses:

```text
models/
└── decision_tree_model.joblib

src/
├── model_config.py
└── model_service.py

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
- creating model input
- making predictions

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
- The model can be integrated into Streamlit through `model_service.py`.

This means the saved model is ready to be used by the Streamlit application without retraining.