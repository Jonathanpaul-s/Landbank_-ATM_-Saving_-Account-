import streamlit as st
import pandas as pd

# App Title
st.title("🌿 Smart Farm AI Dashboard")

# Sidebar Menu
menu = ['Home', 'Disease Detection', 'Fertilizer Recommendation', 'Weather Forecast', 'Crop Yield Prediction']
choice = st.sidebar.selectbox("Select Service", menu)

# Home Page
if choice == 'Home':
    st.image("farm_logo.png", width=350)  # Add your logo image to your project folder
    st.subheader("👋 Welcome to Smart Farm AI")
    st.write("""
        Smart Farm AI is an intelligent farm management platform powered by AI to assist farmers with:
        - 🌱 Crop Disease Detection
        - 🧪 Fertilizer Recommendation
        - ☀️ Weather Forecasting
        - 📈 Crop Yield Prediction
        
        Use the sidebar to access available services.
    """)
    st.success("Developed by Jonathan Paul 🚀")

# Disease Detection Page (placeholder)
elif choice == 'Disease Detection':
    st.subheader("🌱 Crop Disease Detection")
    st.write("Coming Soon")

# Fertilizer Recommendation Page
elif choice == 'Fertilizer Recommendation':
    st.subheader("🧪 Fertilizer Recommendation")

    # User inputs
    crop = st.selectbox("Select Crop", ['Maize', 'Cassava', 'Rice', 'Tomato', 'Yam'])
    soil_type = st.selectbox("Select Soil Type", ['Loamy', 'Sandy', 'Clay', 'Silty'])
    area = st.number_input("Farm Area (hectares)", 1.0, 20.0, step=0.5)
    rainfall = st.number_input("Expected Rainfall (mm)", 300.0, 2000.0, step=10.0)

    if st.button("Get Recommendation"):
        # Simple rule-based logic
        if soil_type == 'Loamy' and rainfall > 1000:
            recommendation = "Use NPK 20:10:10 at 200 kg per hectare"
        elif soil_type == 'Sandy':
            recommendation = "Use NPK 15:15:15 at 150 kg per hectare"
        elif soil_type == 'Clay':
            recommendation = "Use Urea + Organic Manure mix at 180 kg per hectare"
        else:
            recommendation = "Use balanced fertilizer NPK 16:16:16 at 160 kg per hectare"

        st.success(f"🌾 Fertilizer Recommendation: {recommendation}")

# Weather Forecast Page (placeholder)
elif choice == 'Weather Forecast':
    st.subheader("☀️ Weather Forecast")
    st.write("Coming Soon")

# Crop Yield Prediction Page (placeholder)
elif choice == 'Crop Yield Prediction':
    st.subheader("📈 Crop Yield Prediction")
    st.write("Coming Soon")

# Footer
st.markdown("---")
st.markdown("Smart Farm AI | Developed by Jonathan Paul")