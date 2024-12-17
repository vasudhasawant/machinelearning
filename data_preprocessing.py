import pandas as pd

# Load the dataset
data = pd.read_csv('raw_blood_donations.csv')

# Create a target variable (modify this logic based on your needs)
data['target_variable'] = (data['number_of_donations'] > 5).astype(int)  # Example threshold

# Save the cleaned data
data.to_csv('cleaned_blood_donations.csv', index=False)
print("Cleaned data saved as cleaned_blood_donations.csv.")
