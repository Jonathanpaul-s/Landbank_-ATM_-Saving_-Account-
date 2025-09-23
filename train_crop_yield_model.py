import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

# Load the dataset
df = pd.read_csv('crop_yield_dataset.csv')

# Encode the 'Crop' column to numbers
le = LabelEncoder()
df['Crop'] = le.fit_transform(df['Crop'])

# Separate features and target
X = df[['Crop', 'Area (hectares)', 'Rainfall (mm)', 'Fertilizer Used (kg)']]
y = df['Yield (tonnes)']

# Split the dataset into training and testing data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and train the Linear Regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict using the model
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("Model trained successfully!")
print(f"Mean Squared Error: {mse:.2f}")
print(f"R2 Score: {r2:.2f}")