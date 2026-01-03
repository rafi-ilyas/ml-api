import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import joblib

df = pd.read_csv("5000.csv")

X = df[["suhu","kelembapan","cahaya","udara","kebisingan"]]
y = df["label"]

model = DecisionTreeClassifier(max_depth=5)
model.fit(X, y)

joblib.dump(model, "model.pkl")
print("model.pkl berhasil dibuat")

