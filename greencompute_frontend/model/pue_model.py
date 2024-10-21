import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import math
from xgboost import XGBRegressor
import pickle

# Input data\n",
df = pd.read_csv('./US_UE_CZ_Apr14.csv', low_memory=False, index_col=0)
df = df[df['Data Center Size'] != 'Large-Scale']

# Obtain dummy variables
cooling_df = pd.get_dummies(df['Cooling System'])
cooling_types = cooling_df.columns
state_df = pd.get_dummies(df['state_name'])
states = state_df.columns
df[cooling_types] = cooling_df
df[states] = state_df

x_cols = list(cooling_types)
for state in states:
    x_cols.append(state)
    
# Shuffle data    
df = df.sample(frac=1, random_state=42).reset_index(drop=True)
X = df[x_cols]
Y = df['PUE']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

# Initialize and train the model
xgb_model = XGBRegressor(random_state=42)
xgb_model.fit(X_train, y_train)

# Predict and calculate MSE
y_pred_xgb = xgb_model.predict(X_test)
mse_xgb = mean_squared_error(y_test, y_pred_xgb)
print(f"XGBoost MSE: {mse_xgb}, RMSE: {(mse_xgb)**0.5}")

# Save the trained model to a file
with open("xgb_pue_model.pkl", "wb") as file:
    pickle.dump(xgb_model, file)

print("Model training complete and saved to xgb_pue_model.pkl")