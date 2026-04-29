import pandas as pd
import numpy as np
import pickle

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# -----------------------------
# 🔹 LOAD DATA
# -----------------------------
df = pd.read_csv("loan_data.csv")

print("📊 Dataset Loaded Successfully")
print(df.head())

# -----------------------------
# 🔹 HANDLE MISSING VALUES
# -----------------------------
#df.fillna(method='ffill', inplace=True)

# -----------------------------
# 🔹 ENCODE CATEGORICAL DATA
# -----------------------------
df['Gender'] = df['Gender'].map({'Male':1, 'Female':0})
df['Married'] = df['Married'].map({'Yes':1, 'No':0})

df['Employment_Type'] = df['Employment_Type'].map({
    'Salaried':0,
    'Self_Employed':1,
    'Business':2
})

df['Property_Area'] = df['Property_Area'].map({
    'Rural':0,
    'Semiurban':1,
    'Urban':2
})

df['Loan_Status'] = df['Loan_Status'].map({'Y':1, 'N':0})

# -----------------------------
# 🔹 FEATURES & TARGET
# -----------------------------
X = df.drop("Loan_Status", axis=1)
y = df["Loan_Status"]

# -----------------------------
# 🔹 FEATURE SCALING
# -----------------------------
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# -----------------------------
# 🔹 TRAIN TEST SPLIT
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

# -----------------------------
# 🔹 MODEL (STRONGER VERSION)
# -----------------------------
model = RandomForestClassifier(
    n_estimators=300,
    max_depth=8,
    random_state=42
)

model.fit(X_train, y_train)

# -----------------------------
# 🔹 EVALUATION
# -----------------------------
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("\n✅ Model Accuracy:", round(accuracy * 100, 2), "%")

print("\n📊 Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\n📋 Classification Report:")
print(classification_report(y_test, y_pred))

# -----------------------------
# 🔹 FEATURE IMPORTANCE
# -----------------------------
print("\n🔍 Feature Importance:")

feature_names = X.columns
importances = model.feature_importances_

for name, score in zip(feature_names, importances):
    print(f"{name}: {round(score, 3)}")

# -----------------------------
# 🔹 SAVE MODEL & SCALER
# -----------------------------
pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(scaler, open("scaler.pkl", "wb"))

# -----------------------------
# 🔹 SAVE ACCURACY (FOR DASHBOARD)
# -----------------------------
with open("accuracy.txt", "w") as f:
    f.write(str(round(accuracy * 100, 2)))

print("\n💾 Model, Scaler & Accuracy saved successfully!")