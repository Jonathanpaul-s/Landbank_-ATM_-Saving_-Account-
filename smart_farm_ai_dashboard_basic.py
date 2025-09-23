import streamlit as st

# App title
st.title("🚜 Smart Farm AI Dashboard")

# Sidebar navigation
st.sidebar.title("Navigation")
choice = st.sidebar.selectbox("Select Option", ["Home", "Crop Disease Detection", "Weather Forecasting", "Fertilizer Recommendation"])

# Main app logic
if choice == 'Home':
    # Show your logo image
    st.image("farm_logo.png", width=350)

    st.subheader("👋 Welcome to Smart Farm AI")
    st.write("""
        Smart Farm AI is an intelligent farm management platform powered by AI to assist farmers in:
        - Monitoring crop health.
        - Getting real-time weather forecasts.
        - Receiving personalized fertilizer recommendations.
        
        🚀 Boost your farm productivity today!
    """)

elif choice == 'Crop Disease Detection':
    st.subheader("🌾 Crop Disease Detection")
    st.write("🚧 This feature is coming soon... Stay tuned!")

elif choice == 'Weather Forecasting':
    st.subheader("🌦️ Weather Forecasting")
    st.write("🌱 Today's weather forecast for your farm:")
    st.write("Temperature: 28°C")
    st.write("Humidity: 85%")
    st.write("Condition: Cloudy with possible rain in the evening.")

elif choice == 'Fertilizer Recommendation':
    st.subheader("🌱 Fertilizer Recommendation")
    st.write("✅ This feature is already working perfectly!")

else:
    st.error("Invalid Choice. Please select a valid option from the sidebar.")