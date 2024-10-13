import pickle
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor

# Input data
df = pd.read_csv("./Cloud Carbon Footprint - Embodied Emissions.csv")

# Rename columns
df.columns = ['series', 'vm', 'CPU', 'memory', 'carbon_emission', 'carbon_emission2']

# Shuffle and preprocess dataset
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# Features and target variable
X = df[['memory', 'CPU']]  # Memory and CPU as features
y = np.log(df['carbon_emission'])  # Carbon emission as target (log-transformed)

# Split dataset into 80% training and 20% testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the XGBoost model
xgb_model = XGBRegressor(random_state=42)
xgb_model.fit(X_train, y_train)

# Save the trained model to a file
with open("xgb_carbon_model.pkl", "wb") as file:
    pickle.dump(xgb_model, file)

print("Model training complete and saved to xgb_carbon_model.pkl")
