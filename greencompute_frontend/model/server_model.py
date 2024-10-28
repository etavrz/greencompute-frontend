from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.metrics import explained_variance_score
import pandas as pd
import pickle

# Input data
power_ssj_df = pd.read_csv(
    "power_ssj2008-results-20240912-193753.csv", encoding="ISO-8859-1"
)

# Rename columns
power_ssj_df.columns = power_ssj_df.columns.str.strip()
power_ssj_df.columns = power_ssj_df.columns.str.strip().str.replace(
    r"\t", "", regex=True
)

# Performance per core
power_ssj_df["Performance per core @ 50% of target load"] = (
    power_ssj_df["ssj_ops @ 50% of target load"] / power_ssj_df["# Cores"]
)

# Power efficiency #units = performance per watt
power_ssj_df["Power efficiency @ 50% of target load"] = (
    power_ssj_df["ssj_ops @ 50% of target load"]
    / power_ssj_df["Average watts @ 50% of target load"]
)

# Memory efficiency
power_ssj_df["Memory (GB)"] = power_ssj_df["Memory (GB)"].str.replace(
    r"[^\d.]+", "", regex=True
)
power_ssj_df["Memory (GB)"] = pd.to_numeric(
    power_ssj_df["Memory (GB)"], errors="coerce"
)
power_ssj_df["Memory efficiency @ 50% of target load"] = (
    power_ssj_df["Memory (GB)"] / power_ssj_df["ssj_ops @ 50% of target load"]
)

# Cores per memory
power_ssj_df["Cores per memory"] = power_ssj_df["# Cores"] / power_ssj_df["Memory (GB)"]

# RandomForestRegressor
power_ssj_df.dropna(
    subset=["Memory (GB)", "# Cores", "# Chips", "Average watts @ 50% of target load"],
    how="any",
    inplace=True,
)

# Training
X = power_ssj_df[["Memory (GB)", "# Cores", "# Chips"]]
y = power_ssj_df["Average watts @ 50% of target load"]

# Split the data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Initialize the model
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Predictions
y_pred = rf_model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse:.2f}")
print(f"Mean Absolute Error: {mae:.2f}")
print(f"R^2 Score: {r2:.2f}")

explained_variance = explained_variance_score(y_test, y_pred)
print(f"Explained Variance Score: {explained_variance:.2f}")


# Save the trained model to a file
with open("rf_server_model_3vars.pkl", "wb") as file:
    pickle.dump(rf_model, file)

print(
    "Model training complete (3 input variables -- #Cores, #Chips, and Memory) and saved to rf_server_model_3vars.pkl"
)
