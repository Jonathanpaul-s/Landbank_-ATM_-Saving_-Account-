import streamlit as st 



st.set_page_config(
    page_title="Smart Farm AI",
    page_icon="🌾",
    layout="wide"
)

st.title("🌾 Smart Farm AI Dashboard")

menu = st.sidebar.selectbox("Main Menu", [
    "🌿 Farm Management",
    "📊 Productivity & Records",
    "💧 Irrigation & Soil",
    "📅 Calendar & Seasons",
    "🤖 AI Prediction",
    "💡 AI Farm Tips",
    "💹 Market & Economic Toochanged this line to matchis here
]) here
])

# 🏡 HOME
if menu == "🏡 Home":
    st.subheader("Welcome to Smart Farm AI!")
    st.write("Use the sidebar to navigate through available tools.")

# 🌿 FARM MANAGEMENT
elif menu == "🌿 Farm Management":
    option = st.selectbox("Select a Feature", [
        "Farm Equipment Tracker",
        "Pesticides Recommendation",
        "Add Sale Record",
        "Add Order Record",
        "Farm Labor Record",
        "Farm Location Mapper"
    ], key="farm_mgmt")

    if option == "Farm Equipment Tracker":
        st.subheader("Farm Equipment Tracker")
        equipment_name = st.text_input("Enter Equipment Name:")
        purchase_date = st.date_input("Select Purchase Date:")
        status = st.selectbox("Equipment Status", ["Available", "In Use", "Under Repair"])
        if st.button("Save Equipment Record"):
            st.success(f"✅ Saved: {equipment_name} | {purchase_date} | {status}")

    elif option == "Pesticides Recommendation":
        st.subheader("Pesticides Recommendation")
        pest_name = st.text_input("Enter Detected Pest Name:")
        crop_type = st.text_input("Enter Crop Type:")
        severity = st.selectbox("Severity Level", ["Low", "Medium", "High"])
        if st.button("Get Recommendation"):
            st.success(f"Use recommended pesticide for {pest_name} on {crop_type} (Severity: {severity})")

    elif option == "Add Sale Record":
        st.subheader("Add Sale Record")
        crop_name = st.text_input("Enter Crop Name Sold:")
        quantity_sold = st.number_input("Quantity Sold (kg):", min_value=0)
        price_per_kg = st.number_input("Price per kg (₦):", min_value=0)
        sale_date = st.date_input("Sale Date:")
        if st.button("Save Sale Record"):
            total_amount = quantity_sold * price_per_kg
            st.success(f"✅ Sale recorded: {quantity_sold} kg of {crop_name} sold for ₦{total_amount}")

    elif option == "Add Order Record":
        st.subheader("Add Order Record")
        customer_name = st.text_input("Customer Name:")
        product_ordered = st.text_input("Product Ordered:")
        quantity_ordered = st.number_input("Quantity Ordered (kg):", min_value=0)
        expected_delivery = st.date_input("Expected Delivery Date:")
        if st.button("Save Order Record"):
            st.success(f"✅ Order saved: {customer_name} ordered {quantity_ordered} kg of {product_ordered}")

    elif option == "Farm Labor Record":
        st.subheader("Farm Labor Record")
        worker_name = st.text_input("Worker Name:")
        task_assigned = st.text_input("Task Assigned:")
        work_date = st.date_input("Work Date:")
        payment_amount = st.number_input("Payment Amount (₦):", min_value=0)
        if st.button("Save Labor Record"):
            st.success(f"✅ Labor record saved: {worker_name} on {work_date}, Task: {task_assigned}, ₦{payment_amount}")

    elif option == "Farm Location Mapper":
        st.subheader("Farm Location Mapper")
        location_name = st.text_input("Farm Location Name:")
        gps_coordinates = st.text_input("Enter GPS Coordinates (e.g. 7.3775, 3.9470):")
        land_size = st.number_input("Land Size (hectares):", min_value=0.0)
        if st.button("Save Farm Location"):
            st.success(f"✅ Location Saved: {location_name}, GPS:{gps_coordinates}, size:{land_size}hectares")

# 📊 Productivity & Records
 
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
    ], key="productivity")  # key added to prevent duplication

     if option == "View Sales Record":
        st.subheader("View Sales Record")
        st.write("📈 (This will later show all recorded sales in a table here.)")   
     
     elif option == "View Expense":
        st.subheader("View Expense")
        expense_name = st.text_input("Expense Item:")
        expense_amount = st.number_input("Amount Spent (₦):", min_value=0)
        expense_date = st.date_input("Expense Date:")
        if st.button("Save Expense"):
            st.success(f"✅ Expense recorded: {expense_name}, ₦{expense_amount} on {expense_date}") 

     elif option == "Calculate Profit":
        st.subheader("Calculate Profit")
        total_sales = st.number_input("Enter Total Sales (₦):", min_value=0)
        total_expenses = st.number_input("Enter Total Expenses (₦):", min_value= 0)
        if st.button("Calculate Profit"):
            profit = total_sales - total_expenses
            st.success(f"✅ Net Profit:{profit}")

     elif option == "View Farmer Record":
        st.subheader("View Farmer Record")
        st.write("👩‍🌾 (This will later display registered farmers' records here.)")

     elif option == "Farm Productivity":
        st.subheader("Farm Productivity")
        crop_name = st.text_input("Crop Name:")
        season = st.selectbox("Season", ["Dry Season", "Rainy Season"])
        yield_kg = st.number_input("Total Yield (kg):", min_value=0)
        farm_size = st.number_input("Farm Size (hectares):", min_value=0.0)
        if st.button("Record Productivity"):
            st.success(f"✅ Productivity recorded for {crop_name} ({season}): {yield_kg} kg on {farm_size} hectares")

     elif option == "Yield Estimator":
        st.subheader("Yield Estimator")
        farm_area = st.number_input("Farm Area (hectares):", min_value=0.0)
        average_yield_per_hectare = st.number_input("Expected Yield per Hectare (kg):", min_value=0)
        if st.button("Estimate Yield"):
            estimated_yield = farm_area * average_yield_per_hectare
            st.success(f"✅ Estimated Yield: {estimated_yield} kg")

     elif option == "Farm Loan Recorder":
        st.subheader("Farm Loan Recorder")
        lender_name = st.text_input("Lender Name:")
        loan_amount = st.number_input("Loan Amount (₦):", min_value=0)
        interest_rate = st.number_input("Interest Rate (%):", min_value=0.0)
        repayment_period = st.text_input("Repayment Period (e.g. 12 months)")
        if st.button("Record Loan"):
            st.success(f"✅ Loan recorded: ₦{loan_amount} from {lender_name} at {interest_rate}% for {repayment_period}")

     elif option == "Add Loan Record":
        st.subheader("Add Loan Record")
        loan_purpose = st.text_input("Loan Purpose:")
        loan_date = st.date_input("Loan Date:")
        amount = st.number_input("Loan Amount (₦):", min_value=0)
        if st.button("Save Loan Record"):
            st.success(f"✅ Loan for {loan_purpose} of ₦{amount} on {loan_date} saved.")
    
elif menu == "💧 Irrigation & Soil":
    option = st.selectbox("Select a Feature", [
        "Irrigation Schedule",
        "Soil Health Record"
    ], key="irrigation")

    if option == "Irrigation Schedule":
        st.subheader("Irrigation Schedule")

        farm_location = st.text_input("Farm Location:")
        crop_type = st.text_input("Crop Type:")
        irrigation_date = st.date_input("Irrigation Date:")
        volume = st.number_input("Water Volume (liters):", min_value=0)

        if st.button("Save Irrigation Record"):
            st.success(f"✅ Irrigation record saved: {farm_location} | {crop_type} | {irrigation_date} | {volume} liters")

    elif option == "Soil Health Record":
        st.subheader("Soil Health Record")

        farm_location = st.text_input("Farm Location:")
        soil_ph = st.number_input("Soil pH Level:", min_value=0.0, max_value=14.0)
        moisture_content = st.number_input("Moisture Content (%):", min_value=0)
        nutrient_content = st.text_input("Nutrient Content Summary:")
        test_date = st.date_input("Test Date:")

        if st.button("Save Soil Health Record"):
            st.success(f"✅ Soil record saved for {farm_location} on {test_date}")

# 📅 CALENDAR & SEASON PLANNING
elif menu == "📅 Calendar & Season Planning":
    option = st.selectbox("Select a Feature", ["Planting Calendar"], key="calendar")
    if option == "Planting Calendar":
        st.subheader("Planting Calendar")
        crop_name = st.text_input("Crop Name:")
        best_planting_date = st.date_input("Best Planting Date:")
        expected_harvest_date = st.date_input("Expected Harvest Date:")
        season = st.selectbox("Season", ["Dry Season", "Rainy Season", "Harmattan"])
        if st.button("Save Planting Schedule"):
            st.success(f"✅ {crop_name} | Plant: {best_planting_date}{season}")   

#  AI PREDICTIONS & SENSORS   
elif menu == "🧪 AI Predictions & Sensors":
     option = st.selectbox("Select a Feature", [
        "Disease Advice / Crop Disease Detector",
        "Weather Forecasting",
        "Sensor Data (Lot Sensor, Indicator)",
        "AI Decision Making Models"
    ], key="ai_predictions")

     if option == "Disease Advice / Crop Disease Detector":
        st.subheader("Crop Disease Detector")
        crop_type = st.text_input("Crop Type:")
        symptoms = st.text_area("Describe Symptoms:")
        if st.button("Diagnose Disease"):
           st.success(f"✅ AI diagnosis done for {crop_type}. Symptoms: {symptoms}")

     elif option == "Weather Forecasting":
        st.subheader("Weather Forecasting")
        farm_location = st.text_input("Farm Location:")
        if st.button("Get Forecast"):
            st.success(f"✅ Weather forecast for {farm_location} coming soon!")

     elif option == "Sensor Data (Lot Sensor, Indicator)":
        st.subheader("Sensor Data")
        sensor_type = st.selectbox("Sensor Type:", ["Moisture", "Temperature", "pH", "Humidity"])
        sensor_value = st.number_input("Sensor Value:", min_value=0.0)
        record_time = st.date_input("Record Date:")
        if st.button("Save Sensor Reading"):
            st.success(f"✅ {sensor_type} reading of {sensor_value} on {record_time} saved.")

     elif option == "AI Decision Making Models":
        st.subheader("AI Decision Making Models")
        situation = st.text_area("Describe your farm situation:")
        if st.button("Get AI Advice"):
            st.success("✅ AI advice generated for your situation.")

# AI farm tips
elif menu == "💡 AI Farm Tips":
     option = st.selectbox("Select AI Farm Tip Option", [
        "Ask AI Farm Tip",
        "View Daily Farm Tip"
    ], key="ai_tips_option") 
  
     if option == "Ask AI Farm Tip":
        user_tip = st.text_input("Ask your farming question here:", key="ai_tip_input") 
        if st.button("Get AI Tip", key="ai_tip_button"):
            if user_tip:
                # Simulate AI tip response
                st.success(f"✅ AI Farm Tip: Based on your question, consider using organic fertilizer during early growth stage.")
                st.write("🛠️ DEBUG: User question submitted successfully.")
            else:
                st.warning("Please enter a question to get a tip.")
                st.write("🛠️ DEBUG: No question entered.")

     elif option == "View Daily Farm Tip":
        st.info("🌞 Daily Tip: Water your crops early in the morning to reduce evaporation and improve absorption.")
        st.write("🛠️ DEBUGtip displayed.")tip disp

# market & Economic tools 
elif menu == "💹 Market & Economic Tools":
    option = st.selectbox("Select a Market Tool", [
        "Get Market Price",
        "Calculate ROI",
        "Input Cost Estimator"
    ], key="market_tools_option")

    if option == "Get Market Price":
        crop_input = st.text_input("Enter crop name to check current market price:", key="market_price_input")
        if st.button("Check Price", key="check_price_button"):
            if crop_input:
                # Simulated price output (you can replace with scraped or API data later)
                st.success(f"📈 Market Price: The current average market price for {crop_input} is ₦15,000 per 100kg.")
                st.write("🛠️ DEBUG: Market price retrieved successfully.")
            else:
                st.warning("Please enter a crop name to check the price.")
                st.write("🛠️ DEBUG: No crop name entered.")

    elif option == "Calculate ROI":
        investment = st.number_input("Enter your investment amount (₦):", min_value=0.0, key="roi_investment")
        profit = st.number_input("Enter expected profit amount (₦):", min_value=0.0, key="roi_profit")
        if st.button("Calculate ROI", key="calculate_roi_button"):
            if investment > 0:
                roi = (profit - investment) / investment * 100
                st.success(f"📊 ROI: Your Return on Investment is {roi:.2f}%")
                st.write("🛠️ DEBUG: ROI calculated successfully.")
            else:
                st.warning("Investment must be greater than 0.")
                st.write("🛠️ DEBUG: Invalid investment input.")

    elif option == "Input Cost Estimator":
        seeds = st.number_input("Seed cost (₦):", min_value=0.0, key="cost_seeds")
        fertilizer = st.number_input("Fertilizer cost (₦):", min_value=0.0, key="cost_fertilizer")
        labor = st.number_input("Labor cost (₦):", min_value=0.0, key="cost_labor")
        misc = st.number_input("Other costs (₦):", min_value=0.0, key="cost_misc")
        if st.button("Estimate Total Cost", key="estimate_cost_button"):
            total = seeds + fertilizer + labor + misc
            st.success(f"💰 Total Estimated Input Cost: ₦{total:,.2f}")