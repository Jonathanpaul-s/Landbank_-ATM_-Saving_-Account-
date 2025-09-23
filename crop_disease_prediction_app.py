import streamlit as st
import joblib
import numpy as np
from PIL import Image

# Load the trained model and label encoder
model = joblib.load("crop_disease_detector.pkl")
encoder = joblib.load("label_encoder.pkl")

# App title
st.title("Crop Disease Detection App")

# Welcome text
st.write("Welcome to the AI-powered crop disease detection app!")

# User input for symptoms
symptom = st.text_input("Enter the crop disease name (Blight, Rust, Rot, Healthy):")

# Predict button
if st.button("Predict Disease"):
    try:
        # Encode the input disease name into a numeric value
        encoded_symptom = encoder.transform([symptom])

        # Predict using the model (passing encoded numeric value in 2D array)
        prediction = model.predict(np.array([[encoded_symptom[0]]]))

        # Decode the predicted numeric value back to disease name
        disease = encoder.inverse_transform([prediction[0]])[0]

        st.success(f"The predicted disease is: {disease}")

        # Show treatment recommendation
        if disease == "Healthy":
            st.info("No treatment needed. Your crop is healthy.")
        elif disease == "Blight":
            st.warning("Apply fungicide and remove infected plants.")
        elif disease == "Rot":
            st.warning("Improve drainage and apply fungicide.")
        elif disease == "Rust":
            st.warning("Use resistant varieties and spray fungicide.")
        else:
            st.warning("Treatment not available for this disease.")

    except Exception as e:
        st.error(f"An error occurred: {e}")

# Image Upload Feature
st.subheader("Upload a crop image for disease detection (coming soon)")

uploaded_file = st.file_uploader("Choose a crop leaf image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Crop Image", use_column_width=True)
    st.success("Image uploaded successfully! (Image prediction feature coming soon.)")

# Footer caption
st.caption("Developed by Jonathan Paul")