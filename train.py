import pandas as pd 

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