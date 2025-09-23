import streamlit as st
import pickle
import numpy as np
import pandas as pd
from datetime import datetime

# Load trained model
with open('smartfarm_crop_model.pkl', 'rb') as file:
    model = pickle.load(file)

st.title("🌾 SmartFarm AI Assistant")

# Input form
crop = st.selectbox("Select Crop Type", ["Maize", "Yam", "Tomato", "Rice", "Cassava"])
temperature = st.number_input("Temperature (°C)", min_value=10, max_value=50)
moisture = st.number_input("Soil Moisture (%)", min_value=0, max_value=100)

if st.button("Predict Health & Pest Risk"):
    try:
        # Prepare input features
        features = np.array([[temperature, moisture]])
        prediction = model.predict(features)[0]

        # Crop Health Prediction
        if prediction == "Healthy":
            st.success(f"✅ Health Prediction: {prediction}\n\n No action needed. Keep monitoring your crop.")
        elif prediction == "Stressed":
            st.warning(f"⚠️ Health Prediction: {prediction}\n\n Advice: Apply balanced NPK fertilizer, irrigate moderately, remove weeds.")
        elif prediction == "Diseased":
            st.error(f"❌ Health Prediction: {prediction}\n\n Advice: Use recommended pesticide or fungicide immediately.")
        else:
            st.info(f"Prediction: {prediction}")

        # Pest Risk Prediction (simple rule-based)
        if temperature > 35 and moisture > 70:
            pest_risk = "High Risk"
            st.error(f"🐛 Pest Risk: {pest_risk}\n Advice: Apply pesticide or organic neem spray immediately.")
        elif 30 <= temperature <= 35 and 50 <= moisture <= 70:
            pest_risk = "Moderate Risk"
            st.warning(f"🐛 Pest Risk: {pest_risk}\n Advice: Check for insects, use traps or neem spray if needed.")
        else:
            pest_risk = "Low Risk"
            st.success(f"🐛 Pest Risk: {pest_risk}\n No action needed.")

        # Log prediction to CSV
        log_data = pd.DataFrame({
            'Crop': [crop],
            'Temperature': [temperature],
            'Moisture': [moisture],
            'Health Prediction': [prediction],
            'Pest Risk': [pest_risk],
            'DateTime': [datetime.now()]
        })
        log_data.to_csv("prediction_log.csv", mode='a', header=False, index=False)

    except Exception as e:
        st.error("An error occurred while predicting. Please try again.")