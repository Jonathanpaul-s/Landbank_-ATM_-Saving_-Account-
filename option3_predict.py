import streamlit as st
from tensorflow import keras
from keras.preprocessing import image
import numpy as np
from PIL import Image as PILImage

# Load your trained AI model
model = keras.models.load_model("crop_disease_detector.h5")

# Streamlit page setup
st.title("🌿 Crop Disease Detection AI")
st.write("Upload a crop leaf image to detect if it's healthy or diseased.")

# File uploader
uploaded_file = st.file_uploader("Choose a leaf image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display uploaded image
    st.image(uploaded_file, caption="📸 Uploaded Image", use_column_width=True)

    # Save uploaded image to temp file
    with open("temp_image.jpg", "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Preprocess image
    img = image.load_img("temp_image.jpg", target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)

    # Make prediction
    prediction = model.predict(img_array)

    # Display result
    if prediction[0][0] > 0.5:
        st.markdown("### 🌱 Prediction: Diseased ⚠️")
    else:
        st.markdown("### 🌱 Prediction: Healthy ✅")