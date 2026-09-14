import pandas as pd 
import numpy as np
from sklearn.metrics import mean_absolute_error
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor

df = pd.read_csv("data/energydata_complete.csv")

print(df.head())

df["date"] = pd.to_datetime(df["date"])
df["hour"] = df["date"].dt.hour
df["day_of_week"] = df["date"].dt.dayofweek
df["is_weekend"] = df["day_of_week"].isin([5, 6]).astype(int)

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
"is_weekend"
]

x = df[features]
y = df[target]

print(x.head())
print(y.head())

n = len(df)

train_end = int(n * 0.70)
val_end = int(n*0.85)

X_train = x.iloc[:train_end]
y_train = y.iloc[:train_end]

X_val = x.iloc[train_end:val_end]
y_val = y.iloc[train_end:val_end]

X_test = x.iloc[val_end:]
y_test = y.iloc[val_end:]

print("Train:", len(X_train))
print("Validation:", len(X_val))
print("Test:", len(X_test))

baseline_value = y_train.mean()
baseline_predictions = np.full(len(y_val), baseline_value)

print("Baseline value:", baseline_value)
print("Number of baseline predictions:", len(baseline_predictions))

baseline_mae = mean_absolute_error(y_val, baseline_predictions) 

print("Baseline MAE:", baseline_mae) 

linear_model = LinearRegression()

linear_model.fit(X_train, y_train)

linear_predictions = linear_model.predict(X_val)
linear_mae = mean_absolute_error(y_val, linear_predictions)

print("Linear Regression MAE:", linear_mae)

depths = [3, 5, 7, 10]

for depth in depths:
    tree_model = DecisionTreeRegressor(
        max_depth=depth,
        random_state=42
    )

    tree_model.fit(X_train, y_train)

    train_predictions = tree_model.predict(X_train)
    val_predictions = tree_model.predict(X_val)

    train_mae = mean_absolute_error(y_train, train_predictions)
    val_mae = mean_absolute_error(y_val, val_predictions)

    print(
        f"Depth {depth} | "
        f"Train MAE: {train_mae:.2f} | "
        f"Validation MAE: {val_mae:.2f}"
    )

tree_train_predictions = tree_model.predict(X_train)

tree_train_mae = mean_absolute_error(
    y_train,
    tree_train_predictions
)

print("Decision Tree Train MAE:", tree_train_mae)


forest_model = RandomForestRegressor(
n_estimators=100,
random_state=42

)

forest_model.fit(X_train, y_train)
forest_predictions = forest_model.predict(X_val)

forest_mae = mean_absolute_error(y_val, forest_predictions)

print("Random Forest MAE:", forest_mae)

forest_train_predictions = forest_model.predict(X_train)

forest_train_mae = mean_absolute_error(
    y_train,
    forest_train_predictions
)

print("Random Forest Train MAE:", forest_train_mae)
print("Random Forest Validation MAE:", forest_mae)