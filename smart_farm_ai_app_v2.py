import streamlit as st
import pandas as pd
import requests  # Make sure it's at the top

# App Title
st.title("🌿 Smart Farm AI Dashboard")

# Sidebar Menu
menu = ['Home', 'Disease Detection', 'Fertilizer Recommendation', 'Weather Forecast', 'Crop Yield Prediction']
choice = st.sidebar.selectbox("Select Service", menu)

# Home Page
if choice == 'Home':
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

# Weather Forecast Page
elif choice == 'Weather Forecast':
    st.subheader("☀️ Farm Weather Forecast")

    api_key = "a2e8038fb11f70500b36e5a65a58af68"  # ← Your API key

    location = st.text_input("Enter Farm Location (City or Town)")

    if st.button("Get Weather"):
        if location == "":
            st.warning("Please enter a location.")
        else:
            try:
                url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
                response = requests.get(url)
                data = response.json()

                if data['cod'] == 200:
                    temp = data['main']['temp']
                    humidity = data['main']['humidity']
                    wind_speed = data['wind']['speed']
                    weather_description = data['weather'][0]['description']

                    st.success(f"🌡 Temperature: {temp}°C")
                    st.success(f"💧 Humidity: {humidity}%")
                    st.success(f"🌬 Wind Speed: {wind_speed} m/s")
                    st.success(f"🌥 Condition: {weather_description.capitalize()}")
                else:
                    st.error(f"Location not found: {location}")
            except Exception as e:
                st.error(f"Error fetching data: {e}")

# Crop Yield Prediction Page (placeholder)
elif choice == 'Crop Yield Prediction':
    st.subheader("📈 Crop Yield Prediction")
    st.write("Coming Soon")

# Footer
st.markdown("---")
st.markdown("Smart Farm AI | Developed by Jonathan Paul 🚀")