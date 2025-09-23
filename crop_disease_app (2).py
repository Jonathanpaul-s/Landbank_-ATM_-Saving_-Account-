import streamlit as st
import joblib

# Load the trained model
model = joblib.load("crop_disease_detector.pkl")

# App title
st.title("Crop Disease Detection App")

# Welcome text
st.write("Welcome to the AI-powered crop disease detection app!")

# User input for symptoms
symptom = st.text_input("Enter the crop symptom you noticed:")

# Predict button
if st.button("Predict Disease"):
    try:
        prediction = model.predict([symptom])
        disease = prediction[0]

        st.success(f"The predicted disease is: {disease}")

        if disease == "Healthy":
            st.info("No treatment needed. Your crop is healthy.")
        elif disease == "Blight":
            st.warning("Recommended treatment: Apply fungicide and remove infected plants.")
        elif disease == "Rot":
            st.warning("Recommended treatment: Improve drainage and apply fungicide.")
        elif disease == "Rust":
            st.warning("Recommended treatment: Use resistant varieties and spray appropriate fungicide.")
        else:
            st.warning("Treatment recommendation not available for this disease.")

    except Exception as e:
        st.error(f"An error occurred: {e}")

st.caption("Developed by Jonathan Paul")