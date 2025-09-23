import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np

# Load the saved CNN model
model = tf.keras.models.load_model("crop_disease_model.h5")

# Preprocess uploaded image
def preprocess_image(image):
    image = image.resize((32, 32))  # Resize to match training size
    image = np.array(image) / 255.0  # Normalize
    image = np.expand_dims(image, axis=0)  # Add batch dimension
    return image

# Streamlit app interface
st.set_page_config(page_title="Crop Disease Detector", layout="centered")
st.title("🌿 AI Crop Health Checker")
st.write("Upload a crop leaf image to check if it's Healthy or Diseased.")

# File uploader
uploaded_file = st.file_uploader("Upload a crop image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_column_width=True)

    with st.spinner("Analyzing..."):
        processed = preprocess_image(image)
        prediction = model.predict(processed)[0][0]

    # Show result
    if prediction > 0.5:
        st.error("🚨 Diseased Crop Detected!")
    else:
        st.success("✅ Healthy Crop Detected!")

    st.write(f"Confidence Score: `{prediction:.2f}`")