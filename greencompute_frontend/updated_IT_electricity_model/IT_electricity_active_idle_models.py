
###IT Electricity model###
# Import necessary libraries
import numpy as np
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score


#load data 
power_ssj_df = pd.read_csv('power_ssj2008-results-20240912-193753.csv',  encoding = "ISO-8859-1")

# Clean column names by removing trailing spaces and special characters
power_ssj_df.columns = power_ssj_df.columns.str.strip().str.replace(r'\t', '', regex=True)

# Performance per core
power_ssj_df["Performance per core @ 50% of target load"] = power_ssj_df["ssj_ops @ 50% of target load"] / power_ssj_df["# Cores"]

# Power efficiency #units = performance per watt
power_ssj_df["Power efficiency @ 50% of target load"] = power_ssj_df["ssj_ops @ 50% of target load"] / power_ssj_df["Average watts @ 50% of target load"]

# Memory efficiency
power_ssj_df['Memory (GB)'] = power_ssj_df['Memory (GB)'].str.replace(r'[^\d.]+', '', regex=True)
power_ssj_df['Memory (GB)'] = pd.to_numeric(power_ssj_df['Memory (GB)'], errors = 'coerce')
power_ssj_df["Memory efficiency @ 50% of target load"] = power_ssj_df["Memory (GB)"] / power_ssj_df["ssj_ops @ 50% of target load"]

# Cores per memory
power_ssj_df["Cores per memory"] = power_ssj_df["# Cores"] / power_ssj_df["Memory (GB)"]

# RandomForestRegressor 
power_ssj_df.dropna(subset = ["Memory (GB)", "# Cores", "# Chips", "Average watts @ 50% of target load"], 
                    how='any', inplace=True)


X = power_ssj_df[["Memory (GB)", "# Cores", "# Chips"]]
y = power_ssj_df["Average watts @ 50% of target load"]

#split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the model
gb_model = GradientBoostingRegressor(n_estimators=100, random_state=42)
gb_model.fit(X_train, y_train)

# Save the trained GradientBoostingRegressor model
model_pickle_path = "gbr_it_electricity_model.pkl"
with open(model_pickle_path, 'wb') as file:
    pickle.dump(gb_model, file)

print(f"Model saved to {model_pickle_path}")



#####Active Idle Prediction#####
X = power_ssj_df[["Memory (GB)", "# Cores", "# Chips"]]
y = power_ssj_df["Average watts @ active idle"]

#split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#initialize the model
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Save the trained GradientBoostingRegressor model
model_pickle_path = "rf_activeidle_model.pkl"
with open(model_pickle_path, 'wb') as file:
    pickle.dump(gb_model, file)

print(f"Model saved to {model_pickle_path}")





