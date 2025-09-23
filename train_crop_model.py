# train_crop_model.py

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import joblib

# Sample training data
data = {
    'Temperature': [20, 25, 30, 35, 40, 23, 27],
    'Humidity': [60, 65, 70, 75, 80, 62, 68],
    'Moisture': [30, 45, 50, 55, 60, 35, 40],
    'Disease': ['Bacteria', 'Fungus', 'Virus', 'Bacteria', 'Fungus', 'Virus', 'Bacteria']
}

df = pd.DataFrame(data)

# Split features and labels
X = df[['Temperature', 'Humidity', 'Moisture']]
y = df['Disease']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and train model
model = LogisticRegression()
model.fit(X_train, y_train)

# Save trained model to file
joblib.dump(model, 'new_crop_disease_detector.pkl')

print("✅ Model trained and saved successfully!")