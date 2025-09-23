import pandas as pd
import random

# Crop types and health statuses
crops = ["Maize", "Yam", "Tomato", "Rice", "Cassava"]
statuses = ["Healthy", "Stressed", "Diseased"]

# Generate 100 random records
data = {
    "Crop": [random.choice(crops) for _ in range(100)],
    "Temperature (°C)": [random.randint(25, 40) for _ in range(100)],
    "Soil Moisture (%)": [random.randint(30, 80) for _ in range(100)],
    "Health Status": [random.choice(statuses) for _ in range(100)]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv("crop_health_data.csv", index=False)

print("✅ New crop_health_data.csv generated with 100 samples!")