import streamlit as st
import requests
import joblib  # for loading your trained model

# App title
st.title("🚜 Smart Farm AI Dashboard")

# Sidebar navigation
st.sidebar.title("Navigation")
choice = st.sidebar.selectbox(
    "Select Option", 
    ["Home", "Crop Disease Detection", "Weather Forecasting", "Fertilizer Recommendation"]
)

# OpenWeatherMap API key
api_key = "a2e8038fb11f70500b36e5a65a58af68"

# Load model only when needed
def load_model():
    return joblib.load("crop_disease_detector.pkl")

# Home Section
if choice == 'Home':
    st.image("farm_logo.png", width=350)
    st.subheader("👋 Welcome to Smart Farm AI")
    st.write("""
        Smart Farm AI is an intelligent farm management platform powered by AI to assist farmers in:
        - Monitoring crop health.
        - Getting real-time weather forecasts.
        - Receiving personalized fertilizer recommendations.
        
        🚀 Boost your farm productivity today!
    """)

# Crop Disease Detection
elif choice == 'Crop Disease Detection':
    st.subheader("🌾 Crop Disease Detection")

    st.write("Provide the symptom code to predict crop disease:")
    symptom1 = st.number_input("Symptom Code (e.g., 1-5)", min_value=1, max_value=5, value=1)

    if st.button("Predict Disease"):
        model = load_model()
        input_data = [[symptom1]]
        prediction = model.predict(input_data)
        st.success(f"🌱 Predicted Disease: {prediction[0]}")
        st.write(f"📊 Model confidence score: {prediction[0]:.2f}")

# Weather Forecasting
elif choice == 'Weather Forecasting':
    st.subheader("🌦 Weather Forecasting")

    city = st.text_input("Enter your city name")

    if st.button("Get Weather"):
        if city:
            try:
                url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
                response = requests.get(url)
                data = response.json()

                if data["cod"] == 200:
                    temperature = data["main"]["temp"]
                    humidity = data["main"]["humidity"]
                    condition = data["weather"][0]["description"]

                    st.success(f"🌱 Weather forecast for {city.title()}:")
                    st.write(f"Temperature: {temperature}°C")
                    st.write(f"Humidity: {humidity}%")
                    st.write(f"Condition: {condition.title()}")
                else:
                    st.error("City not found. Please check your spelling.")
            except:
                st.error("Failed to fetch weather data. Check your internet connection.")
        else:
            st.warning("Please enter a city name.")

# Fertilizer Recommendation
elif choice == 'Fertilizer Recommendation':
    st.subheader("🌱 Fertilizer Recommendation")

    crop = st.selectbox("Select Crop", ["Maize", "Rice", "Tomato", "Cassava", "Yam"])
    season = st.selectbox("Select Season", ["Rainy", "Dry"])
    soil = st.selectbox("Select Soil Type", ["Loamy", "Clay", "Sandy", "Silty"])

    if st.button("Get Recommendation"):
        if crop == "Maize":
            fertilizer = "NPK 15-15-15"
            quantity = "300kg per hectare"
        elif crop == "Rice":
            fertilizer = "Urea and NPK 20-10-10"
            quantity = "250kg per hectare"
        elif crop == "Tomato":
            fertilizer = "NPK 20-10-10 + Organic manure"
            quantity = "200kg per hectare"
        elif crop == "Cassava":
            fertilizer = "NPK 12-12-17"
            quantity = "350kg per hectare"
        elif crop == "Yam":
            fertilizer = "NPK 20-20-0"
            quantity = "200kg per hectare"
        else:
            fertilizer = "General NPK Mix"
            quantity = "200kg per hectare"

        st.success(f"🌿 Recommended Fertilizer for {crop}: {fertilizer}")
        st.info(f"📦 Application Quantity: {quantity}")

        if season == "Rainy" and soil in ["Clay", "Silty"]:
            st.warning("⚠️ Ensure proper drainage to avoid waterlogging.")