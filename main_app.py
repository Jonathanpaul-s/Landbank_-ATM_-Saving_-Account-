import streamlit as st

st.set_page_config(page_title="Smart Farm AI", page_icon="🌿", layout="wide")

st.title("🌾 Smart Farm AI Dashboard")

menu = st.sidebar.selectbox("📖 Main Menu", [
    "🏡 Home",
    "🌿 Farm Management",
    "📊 Productivity & Records",
    "💧 Irrigation & Soil",
    "📅 Calendar & Season Planning",
    "🧪 AI Predictions & Sensors",
    "📈 Market & Economic Tools",
    "📚 AI Farm Tips & Resources"
])

# Home
if menu == "🏡 Home":
    st.subheader("Welcome to Smart Farm AI!")
    st.write("Use the sidebar to navigate through available tools.")

# Farm Management
elif menu == "🌿 Farm Management":
    option = st.selectbox("Select a Feature", [
        "Farm Equipment Tracker",
        "Pesticides Recommendation",
        "Add Sale Record",
        "Add Order Record",
        "Farm Labor Record",
        "Farm Location Mapper"
    ], key="farm_management")

    if option == "Farm Equipment Tracker":
        st.subheader("Farm Equipment Tracker")
        st.write("🔧 Track and manage your farm equipment inventory, status, and maintenance history.")

    elif option == "Pesticides Recommendation":
        st.subheader("Pesticides Recommendation")
        st.write("🦟 Get AI-based pesticide suggestions based on pest types and crop conditions.")

    elif option == "Add Sale Record":
        st.subheader("Add Sale Record")
        st.write("💸 Record produce sales: crop, quantity, price, and date.")

    elif option == "Add Order Record":
        st.subheader("Add Order Record")
        st.write("📦 Log new customer orders with details and delivery dates.")

    elif option == "Farm Labor Record":
        st.subheader("Farm Labor Record")
        st.write("👨‍🌾 Record labor attendance, roles, and payment info.")

    elif option == "Farm Location Mapper":
        st.subheader("Farm Location Mapper")
        st.write("🗺 Map and store GPS location and size of each farm.")

# Productivity & Records
elif menu == "📊 Productivity & Records":
    option = st.selectbox("Select a Feature", [
        "View Sales Record",
        "View Expense",
        "Calculate Profit",
        "View Farmer Record",
        "Farm Productivity",
        "Yield Estimator",
        "Farm Loan Recorder",
        "Add Loan Record"
    ], key="productivity_records")

    if option == "View Sales Record":
        st.subheader("View Sales Record")
        st.write("📈 Review sales records by date, crop, and amount.")

    elif option == "View Expense":
        st.subheader("View Expense")
        st.write("💰 View all operational expenses.")

    elif option == "Calculate Profit":
        st.subheader("Calculate Profit")
        st.write("🧮 Automatically calculate net farm profit.")

    elif option == "View Farmer Record":
        st.subheader("View Farmer Record")
        st.write("👩‍🌾 See registered farmer details and assignments.")

    elif option == "Farm Productivity":
        st.subheader("Farm Productivity")
        st.write("📊 Analyze yield and productivity across seasons.")

    elif option == "Yield Estimator":
        st.subheader("Yield Estimator")
        st.write("🌾 Estimate potential yield using land and soil data.")

    elif option == "Farm Loan Recorder":
        st.subheader("Farm Loan Recorder")
        st.write("💸 Record and monitor loan disbursements and repayments.")

    elif option == "Add Loan Record":
        st.subheader("Add Loan Record")
        st.write("➕ Add a new loan with terms and lender information.")

# Irrigation & Soil
elif menu == "💧 Irrigation & Soil":
    option = st.selectbox("Select a Feature", [
        "Irrigation Schedule",
        "Soil Health Record"
    ], key="irrigation_soil")

    if option == "Irrigation Schedule":
        st.subheader("Irrigation Schedule")
        st.write("💧 Plan and monitor irrigation by time, field, and water volume.")

    elif option == "Soil Health Record":
        st.subheader("Soil Health Record")
        st.write("🌱 Record soil health metrics like pH, moisture, and nutrients.")

# Calendar & Season Planning
elif menu == "📅 Calendar & Season Planning":
    option = st.selectbox("Select a Feature", [
        "Planting Calendar"
    ], key="calendar_season")

    if option == "Planting Calendar":
        st.subheader("Planting Calendar")
        st.write("📆 Schedule crop planting by season and weather forecasts.")

# AI Predictions & Sensors
elif menu == "🧪 AI Predictions & Sensors":
    option = st.selectbox("Select a Feature", [
        "Crop Disease Detector",
        "Weather Forecasting",
        "Sensor Data",
        "AI Decision Making Models"
    ], key="ai_predictions")

    if option == "Crop Disease Detector":
        st.subheader("Crop Disease Detector")
        st.write("🧪 Detect crop diseases using AI models and get treatment tips.")

    elif option == "Weather Forecasting":
        st.subheader("Weather Forecasting")
        st.write("🌦 View local weather forecasts for farming activity planning.")

    elif option == "Sensor Data":
        st.subheader("Sensor Data (IoT Sensor, Indicators)")
        st.write("🤖 Monitor real-time sensor data like soil moisture, temperature.")

    elif option == "AI Decision Making Models":
        st.subheader("AI Decision Models")
        st.write("📊 Use predictive models to assist farm decision making.")

# Market & Economic Tools
elif menu == "📈 Market & Economic Tools":
    option = st.selectbox("Select a Feature", [
        "Market Price Checker",
        "Budget Planner"
    ], key="market_tools")

    if option == "Market Price Checker":
        st.subheader("Market Price Checker")
        st.write("📊 View market prices for crops from local or export markets.")

    elif option == "Budget Planner":
        st.subheader("Budget Planner")
        st.write("📝 Create seasonal financial plans for income and expenses.")

# AI Farm Tips & Resources
elif menu == "📚 AI Farm Tips & Resources":
    option = st.selectbox("Select a Feature", [
        "Show Farm Tip"
    ], key="farm_tips")

    if option == "Show Farm Tip":
        st.subheader("Farm Tips and Best Practices")
        st.write("💡 Get daily or seasonal AI-powered tips for farm improvement.")