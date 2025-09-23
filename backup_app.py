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
    ])
 
    if option == "Farm Equipment Tracker":
      st.subheader("Farm Equipment Tracker")     
      st.write("🔧 Track, record, and manage your farm equipment inventory including status, purchase date, and maintenance hipment.")

    elif option == "Pesticides Recommendation":
        st.subheader("Pesticides Recommendation")
        st.write("🦟 Get AI-based recommendations on the right pesticides to use based on detected pests, crop type, application.")

    elif option == "Add Sale Record":
        st.subheader("Add Sale Record")
        st.write("💸 Record sales transactions for harvested farm produce, including crop type, quantity sold, price, ar harvested crops.")

    elif option == "Add Order Record":
        st.subheaer("Add Order Record")
        st.write("📦 Log new customer orders for farm produce and track order details, expected delivery date, rd new customer orders.")

    elif option == "Farm Labor Record":
        st.subheader("Farm Labor Record")
        st.write("👨‍🌾 Manage farm workers’ attendance, job responsibilities, and payment re Manage farm worker records.")

    elif option == "Farm Location Mapper":
        st.subheader("Farm Location Mapper")
        st.write("🗺️ Record and visualize the GPS location and size of each fnd visualize your farm locations.")

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
    ])

    if option == "View Sales Record":
       st.subheader("View Sales Record")
       st.write("📈 Access and review all farm produce sales records organized by date,crop type,and total sales value.")
        
    elif option == "view Expense":               
        st.subheader("View Expense")
        st.write("💰 Track and view all farm operation expenses such as labor, equipment, fertizers and transportation.")
   
    elif option == "calculate profit":           
         st.subheader("Calculate Profit")
         st.write("🧮 Automatically calculate  your net farm profit by comparing total sales against total expenses.")

    elif option == "view farmer Record":       
        st.subheader("View Farmer Record")
        st.write("👩‍🌾 View records of farmers registered  under your  management including personal details and assigned tasks.")
    
    elif option == "Farm Productivity":        
        st.subheader("Farm Productivity")
        st.write("📊 Track and analyze your farm’s productivity per season or per crop, measuring total yield and harvest rate.")
        
    elif option == "Yield Estimator":        
        st.subheader("Yield Estimator")
        st.write("🌾 Estimate potential yield for each farm plot based on land size,soil condition,and expected crop performance.")
    
    if option == "Farm Loan Recorder":
       st.subheader("Farm Loan Recorder")
       st.write("💸 Record farm loans,monitor disbursement, repayment schedule, and oustanding balances.")
                 
    elif option == "Add Loan Record":
        st.subheader("Add Loan Record")
        st.write("➕ Add new loan details including lender name,amount,interest rate, repayment peroid, and purpose.") 

# Irrigation & Soil
elif menu == "💧 Irrigation & Soil":
    option = st.selectbox("Select a Feature", [
        "Irrigation schedule",
        "soil Health Record"
    ])

    if option == "Irrigation Schedule":
       st.subheader("Irrigation Schedule")
       st.write("💧 Plan and monitor your farm's irrigation schedules,tracking watering times,volumes,and field conditions.")
        
    elif option == "Soil Health Record":
         st.subheader("Soil Health Record")
         st.write("🌱 Record soil test results, nutrient content, pH levels, and moisture data for each farm location.")

# Calendar & Season Planning
elif menu == "📅 Calendar & Season Planning":
    option = st.selectbox("Select a Feature", [
        "Planting Calendar"
    ])

    if option == "planting calendar": 
       st.subheader("Planting Calendar")
       st.Write("📆 schedule planting dates for different crops based on best seasonal practices and weather predictions.")

# AI Predictions & Sensors
elif menu == "🧪 AI Predictions & Sensors":
    option = st.selectbox("Select a Feature", [
        "Disease Advice / Crop Disease Detector",
        "Weather Forecasting",       
        "Sensor Data (Lot Sensor, Indicator)",
        "AI Decision Making Models"
    ])

    if option == "Disease Advice/Crop Disease Detector":
       st.subheader("Crop Disease Detector")
       st.write("🧪Detect crop disease early using AI model based on syptoms or image analysis and recieve treatment reccommendations.")

    elif option == " Weather Forcasting":
       st.subheader("Weather Forecasting")
       st.write("🌦️ Access up to date weather predictions tailored for your farm location to plan activities like planting,fertilizing,and harvesting.")
        
    elif option == "Sensor Data": 
        st.subheader("Sensor Data (Lot Sensor, Indicator)")
        st.write("🤖 Monitor real time farm sensor reading such as soil moisture,temperature,and humidity using connected LOT devices.")

# Market & Economic Tools
elif menu == "📈 Market & Economic Tools":
    option = st.selectbox("Select a Feature", [
        "Market price checker",
          "Budget Planner"
 ])

    if option == "Market Price Checker":
        st.subheader("Market Price Checker")        
        st.write("📊 View current market prices for various farm produce across neaby markets and export points.")

    elif option == "Budget Planner":
        st.subheader("Budget Planner")
        st.write("Plan manage your farm's financial budget for each season,covering expenses,loans,and expected income.")


# AI Farm Tips & Resources
elif menu == "📚 AI Farm Tips & Resources":
    option = st.selectbox("select a feature",[
         " Show farm Tip"
    
    ])
           
    if option == "Show Farm Tip":
        st.subheader("Farm Tips and Best Practices")
        st.write("💡 Access AI generated daily or seasonal farm tips, productivity hacks, and agricultural advice for better yields.")

