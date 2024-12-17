import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load your data (ensure this path is correct)
data = pd.read_csv('raw_blood_donations.csv')  # Adjust as necessary
X = data[['months_since_last_donation', 'months_since_first_donation', 'number_of_donations']]
y = data['target_variable']

# Train the model
model = RandomForestClassifier()  # Adjust model parameters as needed
model.fit(X, y)

# Save the model
joblib.dump(model, 'blood_donation_model.pkl')
print("Model trained and saved successfully.")
