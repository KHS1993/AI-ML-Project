import pandas as pd
import numpy as np
import joblib

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from src.model_config import FEATURE_COLUMNS, MODEL_PATH

# --------------------------------------------------
# 1. Läs in data
# --------------------------------------------------

df = pd.read_csv("data/energydata_complete.csv")

df["date"] = pd.to_datetime(df["date"])


# --------------------------------------------------
# 2. Feature engineering från datum
# --------------------------------------------------

df["hour"] = df["date"].dt.hour
df["day_of_week"] = df["date"].dt.dayofweek
df["is_weekend"] = df["day_of_week"].isin([5, 6]).astype(int)


# --------------------------------------------------
# 3. Definiera target och features
# --------------------------------------------------

target = "Appliances"


X = df[FEATURE_COLUMNS]
y = df[target]


# --------------------------------------------------
# 4. Tidsbaserad train / validation / test-split
# --------------------------------------------------

n = len(df)

train_end = int(n * 0.70)
val_end = int(n * 0.85)

X_train = X.iloc[:train_end]
y_train = y.iloc[:train_end]

X_val = X.iloc[train_end:val_end]
y_val = y.iloc[train_end:val_end]

X_test = X.iloc[val_end:]
y_test = y.iloc[val_end:]

print("\nData split")
print("Train:", len(X_train))
print("Validation:", len(X_val))
print("Test:", len(X_test))


# --------------------------------------------------
# 5. Baseline
# --------------------------------------------------

baseline_value = y_train.mean()

baseline_val_predictions = np.full(
    len(y_val),
    baseline_value,
)

baseline_val_mae = mean_absolute_error(
    y_val,
    baseline_val_predictions,
)

baseline_val_rmse = np.sqrt(
    mean_squared_error(
        y_val,
        baseline_val_predictions,
    )
)

baseline_val_r2 = r2_score(
    y_val,
    baseline_val_predictions,
)


# --------------------------------------------------
# 6. Linear Regression
# --------------------------------------------------

linear_model = LinearRegression()

linear_model.fit(
    X_train,
    y_train,
)

linear_val_predictions = linear_model.predict(X_val)

linear_val_mae = mean_absolute_error(
    y_val,
    linear_val_predictions,
)

linear_val_rmse = np.sqrt(
    mean_squared_error(
        y_val,
        linear_val_predictions,
    )
)

linear_val_r2 = r2_score(
    y_val,
    linear_val_predictions,
)

# --------------------------------------------------
# 7. Decision Tree
# --------------------------------------------------

tree_model = DecisionTreeRegressor(
    max_depth=7,
    random_state=42,
)

tree_model.fit(
    X_train,
    y_train,
)

MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)

joblib.dump(
    tree_model,
    MODEL_PATH,
)

print(f"\nSaved model to: {MODEL_PATH}")

loaded_tree_model = joblib.load(MODEL_PATH)

original_predictions = tree_model.predict(X_val)
loaded_predictions = loaded_tree_model.predict(X_val)

predictions_match = np.array_equal(
    original_predictions,
    loaded_predictions,
)

print("Loaded model predictions match:", predictions_match)

if not predictions_match:
    raise RuntimeError(
        "Loaded model predictions do not match the original model."
    )

tree_train_predictions = tree_model.predict(X_train)
tree_val_predictions = tree_model.predict(X_val)

tree_train_mae = mean_absolute_error(
    y_train,
    tree_train_predictions,
)

tree_val_mae = mean_absolute_error(
    y_val,
    tree_val_predictions,
)

tree_train_rmse = np.sqrt(
    mean_squared_error(
        y_train,
        tree_train_predictions,
    )
)

tree_val_rmse = np.sqrt(
    mean_squared_error(
        y_val,
        tree_val_predictions,
    )
)

tree_train_r2 = r2_score(
    y_train,
    tree_train_predictions,
)

tree_val_r2 = r2_score(
    y_val,
    tree_val_predictions,
)

# --------------------------------------------------
# 8. Random Forest
# --------------------------------------------------

forest_model = RandomForestRegressor(
    n_estimators=100,
    random_state=42,
)

forest_model.fit(
    X_train,
    y_train,
)

forest_train_predictions = forest_model.predict(X_train)
forest_val_predictions = forest_model.predict(X_val)

forest_train_mae = mean_absolute_error(
    y_train,
    forest_train_predictions,
)

forest_val_mae = mean_absolute_error(
    y_val,
    forest_val_predictions,
)

forest_train_rmse = np.sqrt(
    mean_squared_error(
        y_train,
        forest_train_predictions,
    )
)

forest_val_rmse = np.sqrt(
    mean_squared_error(
        y_val,
        forest_val_predictions,
    )
)

forest_train_r2 = r2_score(
    y_train,
    forest_train_predictions,
)

forest_val_r2 = r2_score(
    y_val,
    forest_val_predictions,
)

# --------------------------------------------------
# 9. Jämför modeller på validation-data
# --------------------------------------------------

results = pd.DataFrame({
    "Model": [
        "Baseline",
        "Linear Regression",
        "Decision Tree",
        "Random Forest",
    ],
    "Validation MAE": [
        baseline_val_mae,
        linear_val_mae,
        tree_val_mae,
        forest_val_mae,
    ],
    "Validation RMSE": [
        baseline_val_rmse,
        linear_val_rmse,
        tree_val_rmse,
        forest_val_rmse,
    ],
    "Validation R2": [
        baseline_val_r2,
        linear_val_r2,
        tree_val_r2,
        forest_val_r2,
    ],
})

print("\nModel comparison")
print(results)

# --------------------------------------------------
# 10. Kontrollera overfitting
# --------------------------------------------------

print("\nDecision Tree - Train vs validation")

print(f"Train MAE: {tree_train_mae:.2f}")
print(f"Validation MAE: {tree_val_mae:.2f}")

print(f"Train RMSE: {tree_train_rmse:.2f}")
print(f"Validation RMSE: {tree_val_rmse:.2f}")

print(f"Train R2: {tree_train_r2:.3f}")
print(f"Validation R2: {tree_val_r2:.3f}")


print("\nRandom Forest - Train vs validation")

print(f"Train MAE: {forest_train_mae:.2f}")
print(f"Validation MAE: {forest_val_mae:.2f}")

print(f"Train RMSE: {forest_train_rmse:.2f}")
print(f"Validation RMSE: {forest_val_rmse:.2f}")

print(f"Train R2: {forest_train_r2:.3f}")
print(f"Validation R2: {forest_val_r2:.3f}")


# --------------------------------------------------
# 11. Sluttest av vald modell
# --------------------------------------------------

tree_test_predictions = tree_model.predict(X_test)

tree_test_mae = mean_absolute_error(
    y_test,
    tree_test_predictions,
)

tree_test_rmse = np.sqrt(
    mean_squared_error(
        y_test,
        tree_test_predictions,
    )
)

tree_test_r2 = r2_score(
    y_test,
    tree_test_predictions,
)

baseline_test_predictions = np.full(
    len(y_test),
    baseline_value,
)

baseline_test_mae = mean_absolute_error(
    y_test,
    baseline_test_predictions,
)

baseline_test_rmse = np.sqrt(
    mean_squared_error(
        y_test,
        baseline_test_predictions,
    )
)

baseline_test_r2 = r2_score(
    y_test,
    baseline_test_predictions,
)

print("\nSelected model test performance")

print("\nBaseline")
print(f"MAE: {baseline_test_mae:.2f} Wh")
print(f"RMSE: {baseline_test_rmse:.2f} Wh")
print(f"R2: {baseline_test_r2:.3f}")

print("\nDecision Tree")
print(f"MAE: {tree_test_mae:.2f} Wh")
print(f"RMSE: {tree_test_rmse:.2f} Wh")
print(f"R2: {tree_test_r2:.3f}")

# --------------------------------------------------
# 12. Enkel analys av distribution shift
# --------------------------------------------------

print("\nAppliances mean by split")

print(
    "Train:",
    y_train.mean(),
)

print(
    "Validation:",
    y_val.mean(),
)

print(
    "Test:",
    y_test.mean(),
)


print("\nT_out mean by split")

print(
    "Train:",
    X_train["T_out"].mean(),
)

print(
    "Validation:",
    X_val["T_out"].mean(),
)

print(
    "Test:",
    X_test["T_out"].mean(),
)


print("\nT_out statistics")

print("\nTrain:")
print(
    X_train["T_out"].describe()
)

print("\nValidation:")
print(
    X_val["T_out"].describe()
)

print("\nTest:")
print(
    X_test["T_out"].describe()
)