import pandas as pd 
import numpy as np
from sklearn.metrics import mean_absolute_error
from sklearn.linear_model import LinearRegression

df = pd.read_csv("data/energydata_complete.csv")

print(df.head())

df["date"] = pd.to_datetime(df["date"])

target = "Appliances"

features = [
"T1",
"RH_1",
"T2",
"RH_2",
"T_out",
"RH_out"
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