import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
import joblib

# Sample dataset — replace this with your actual CSV or data
data = pd.DataFrame({
    'Symptom': ['yellow spots', 'brown patches', 'dry leaves', 'wilting stem', 'no issue'],
    'Disease': ['Blight', 'Rust', 'Rot', 'Rot', 'Healthy']
})

# Encode disease labels into numeric values
encoder = LabelEncoder()
data['DiseaseEncoded'] = encoder.fit_transform(data['Disease'])

# Train the model (simple logistic regression for demo)
model = LogisticRegression()
model.fit(data[['Symptom']].apply(lambda x: x.factorize()[0]), data['DiseaseEncoded'])

# Save model and encoder
joblib.dump(model, "crop_disease_detector.pkl")
joblib.dump(encoder, "label_encoder.pkl")

print("Model and encoder saved successfully.")