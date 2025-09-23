import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np

# Load model (only once using caching)
@st.cache_resource
def load_model():
    return tf.keras.models.load_model("crop_disease_model.h5")

model = load_model()

# Preprocess uploaded image
def preprocess_image(image):
    image = image.resize((32, 32))  # Resize to match training size
    image = np.array(image) / 255.0  # Normalize
    image = np.expand_dims(image, axis=0)  # Add batch dimension
    return image

# Streamlit App UI
st.set_page_config(page_title="Option 3 - Predict One Image", layout="centered")
st.title("🌿 Option 3: Crop Health Prediction")
st.write("Upload a crop leaf image to check if it's Healthy or Diseased.")

uploaded_file = st.file_uploader("Choose a crop image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_column_width=True)

    with st.spinner("Analyzing Image..."):
        processed_image = preprocess_image(image)
        prediction = model.predict(processed_image)[0][0]

    if prediction > 0.5:
        st.error("🚨 Diseased Crop Detected!")
    else:
        st.success("✅ Healthy Crop Detected!")

    st.write(f"Model Confidence Score: `{prediction:.2f}`")