import streamlit as st
import pandas as pd
import numpy as np
import pickle

# Title
st.title("🌿 Smart Farm AI Dashboard")

# Sidebar navigation
menu = ['Home', 'Disease Detection', 'Fertilizer Recommendation', 'Weather Forecast', 'Crop Yield Prediction']
choice = st.sidebar.selectbox("Select Service", menu)

# Home page
if choice == 'Home':
    st.subheader("👋 Welcome to Smart Farm AI")
    st.write("Use the sidebar to access various AI farm management tools.")

# Disease Detection page (placeholder)
elif choice == 'Disease Detection':
    st.subheader("🌱 Crop Disease Detection")
    st.write("Upload an image or enter crop details for disease detection. (Coming Soon)")

# Fertilizer Recommendation page (placeholder)
elif choice == 'Fertilizer Recommendation':
    st.subheader("🧪 Fertilizer Recommendation")
    st.write("Input soil data, crop type, and farm conditions to get fertilizer advice. (Coming Soon)")

# Weather Forecast page (placeholder)
elif choice == 'Weather Forecast':
    st.subheader("☀️ Weather Forecast")
    st.write("View current and upcoming farm weather conditions. (Coming Soon)")

# Crop Yield Prediction page
elif choice == 'Crop Yield Prediction':
    st.subheader("📈 Predict Crop Yield")

    # User inputs
    crop = st.selectbox("Select Crop", ['Maize', 'Cassava', 'Rice', 'Tomato', 'Yam'])
    area = st.number_input("Farm Area (hectares)", 1.0, 20.0, step=0.5)
    rainfall = st.number_input("Rainfall (mm)", 300.0, 2000.0, step=10.0)
    fertilizer = st.number_input("Fertilizer Used (kg)", 50.0, 500.0, step=10.0)

    if st.button("Predict Yield"):
        try:
            # Encode crop manually
            crop_mapping = {'Maize': 0, 'Cassava': 1, 'Rice': 2, 'Tomato': 3, 'Yam': 4}
            crop_encoded = crop_mapping[crop]

            # Load the trained model
            with open("crop_yield_model.pkl", "rb") as file:
                model = pickle.load(file)

            # Create input array
            input_data = np.array([[crop_encoded, area, rainfall, fertilizer]])

            # Make prediction
            prediction = model.predict(input_data)[0]

            # Show result
            st.success(f"🌾 Estimated Crop Yield: {prediction:.2f} tonnes")
            st.write(f"Model confidence score: {prediction:.2f}")

        except FileNotFoundError:
            st.error("Model file not found. Please ensure 'crop_yield_model.pkl' exists in the same folder.")
        except Exception as e:
            st.error(f"An error occurred: {e}")