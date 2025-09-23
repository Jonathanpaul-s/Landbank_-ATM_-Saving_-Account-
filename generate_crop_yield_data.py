import pandas as pd
import numpy as np

# Simulate crop yield dataset
data = {
    'Crop': np.random.choice(['Maize', 'Cassava', 'Rice', 'Tomato', 'Yam'], 30),
    'Area (hectares)': np.random.uniform(1, 10, 30).round(2),
    'Rainfall (mm)': np.random.uniform(500, 1500, 30).round(2),
    'Fertilizer Used (kg)': np.random.uniform(100, 300, 30).round(2),
    'Yield (tonnes)': np.random.uniform(2, 10, 30).round(2)
}

df = pd.DataFrame(data)

# Save dataset to CSV file
df.to_csv('crop_yield_dataset.csv', index=False)

print(df.head())