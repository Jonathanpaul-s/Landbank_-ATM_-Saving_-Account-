import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import pickle

# Load the dataset
data = pd.read_csv('crop_health_data.csv')

# Prepare the features (Temperature and Soil Moisture) and the target (Health Status)
X = data[['Temperature (°C)', 'Soil Moisture (%)']]
y = data['Health Status']

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the Logistic Regression model
model = LogisticRegression(max_iter=200)

# Train the model
model.fit(X_train, y_train)

# Save the trained model as a pickle file
with open('smartfarm_crop_model.pkl', 'wb') as file:
    pickle.dump(model, file)

print("✅ Model trained and saved successfully!")