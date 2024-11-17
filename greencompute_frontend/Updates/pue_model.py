import pickle

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from xgboost import XGBRegressor

# Input data
df = pd.read_csv("./US_UE_CZ_Apr14.csv", low_memory=False, index_col=0)
df = df[df["Data Center Size"] != "Large-Scale"]

# Define the feature columns
cooling_types = df["Cooling System"].unique()
states = df["state_name"].unique()

# Prepare target variable (y) and features (X)
X = df[["Cooling System", "state_name"]]
y = df["PUE"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define preprocessing: OneHotEncoder for categorical columns
preprocessor = ColumnTransformer(
    transformers=[
        ("cooling", OneHotEncoder(), ["Cooling System"]),
        ("state", OneHotEncoder(), ["state_name"]),
    ]
)

# Define the pipeline: Preprocessing + Model (XGBoost)
pipeline = Pipeline(steps=[("preprocessor", preprocessor), ("regressor", XGBRegressor(random_state=42))])

# Train the model
pipeline.fit(X_train, y_train)

# Predict and calculate MSE
y_pred_xgb = pipeline.predict(X_test)
mse_xgb = mean_squared_error(y_test, y_pred_xgb)
print(f"XGBoost MSE: {mse_xgb}, RMSE: {(mse_xgb)**0.5}")

# Save the trained model to a file
with open("xgb_pue_sklearn.pkl", "wb") as file:
    pickle.dump(pipeline, file)

print("Model training complete and saved to xgb_pue_sklearn.pkl")
