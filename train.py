import pandas as pd
import numpy as np

from sklearn.metrics import mean_absolute_error
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor


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

features = [
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

X = df[features]
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

baseline_predictions = np.full(
    len(y_val),
    baseline_value
)

baseline_mae = mean_absolute_error(
    y_val,
    baseline_predictions
)


# --------------------------------------------------
# 6. Linear Regression
# --------------------------------------------------

linear_model = LinearRegression()

linear_model.fit(
    X_train,
    y_train
)

linear_predictions = linear_model.predict(X_val)

linear_mae = mean_absolute_error(
    y_val,
    linear_predictions
)


# --------------------------------------------------
# 7. Decision Tree
# --------------------------------------------------

tree_model = DecisionTreeRegressor(
    max_depth=7,
    random_state=42
)

tree_model.fit(
    X_train,
    y_train
)

tree_train_predictions = tree_model.predict(X_train)
tree_val_predictions = tree_model.predict(X_val)

tree_train_mae = mean_absolute_error(
    y_train,
    tree_train_predictions
)

tree_val_mae = mean_absolute_error(
    y_val,
    tree_val_predictions
)


# --------------------------------------------------
# 8. Random Forest
# --------------------------------------------------

forest_model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

forest_model.fit(
    X_train,
    y_train
)

forest_train_predictions = forest_model.predict(X_train)
forest_val_predictions = forest_model.predict(X_val)

forest_train_mae = mean_absolute_error(
    y_train,
    forest_train_predictions
)

forest_val_mae = mean_absolute_error(
    y_val,
    forest_val_predictions
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
        baseline_mae,
        linear_mae,
        tree_val_mae,
        forest_val_mae,
    ],
})

print("\nModel comparison")
print(results)


# --------------------------------------------------
# 10. Kontrollera overfitting
# --------------------------------------------------

print("\nTrain vs validation")

print(
    "Decision Tree Train MAE:",
    tree_train_mae
)

print(
    "Decision Tree Validation MAE:",
    tree_val_mae
)

print(
    "Random Forest Train MAE:",
    forest_train_mae
)

print(
    "Random Forest Validation MAE:",
    forest_val_mae
)


# --------------------------------------------------
# 11. Sluttest av vald modell
# --------------------------------------------------

tree_test_predictions = tree_model.predict(X_test)

tree_test_mae = mean_absolute_error(
    y_test,
    tree_test_predictions
)

print("\nSelected model test performance")
print(
    "Decision Tree Test MAE:",
    tree_test_mae
)


# --------------------------------------------------
# 12. Enkel analys av distribution shift
# --------------------------------------------------

print("\nAppliances mean by split")

print(
    "Train:",
    y_train.mean()
)

print(
    "Validation:",
    y_val.mean()
)

print(
    "Test:",
    y_test.mean()
)


print("\nT_out mean by split")

print(
    "Train:",
    X_train["T_out"].mean()
)

print(
    "Validation:",
    X_val["T_out"].mean()
)

print(
    "Test:",
    X_test["T_out"].mean()
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