import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Load your data
data = pd.read_csv('raw_blood_donations.csv')
X = data[['months_since_last_donation', 'months_since_first_donation', 'number_of_donations']]
y = data['target_variable']  # Ensure target variable is continuous for regression

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Initialize models
models = {
    "Random Forest": RandomForestRegressor(),
    "Linear Regression": LinearRegression(),
    "K-Nearest Neighbors": KNeighborsRegressor(),
    "Support Vector Regressor": SVR()
}

# Calculate metrics and save to a CSV file
metrics_data = []
for name, model in models.items():
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    metrics_data.append({
        'Model': name,
        'MAE': mean_absolute_error(y_test, predictions),
        'MSE': mean_squared_error(y_test, predictions),
        'R2 Score': r2_score(y_test, predictions)
    })

# Convert to DataFrame and save to CSV
metrics_df = pd.DataFrame(metrics_data)
metrics_df.to_csv('regression_metrics.csv', index=False)
print("Metrics saved to regression_metrics.csv")
