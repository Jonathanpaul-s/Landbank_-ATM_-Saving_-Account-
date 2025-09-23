import streamlit as st 



st.set_page_config(
    page_title="Smart Farm AI",
    page_icon="🌾",
    layout="wide"
)

menu = st.sidebar.selectbox("Main Menu", [
    "🌿 Farm Management",
    "📊 Productivity & Records",
    "💧 Irrigation & Soil",
    "📅 Calendar & Seasons",
    "🤖 AI Prediction",
    "💡 AI Farm Tips",
    "💹 Market & Economic Tools"  # <--- add this here
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
            st.success(f"✅ Soil record saved for {farm_location} on  {test_date}")
 
# 📅 Calendar & Seasons
elif menu == "📅 Calendar & Seasons":
    option = st.selectbox("Select a Calendar Tool", [
        "Planting Calendar",
        "Harvest Time Estimator",
        "Seasonal Task Planner"
    ], key="calendar_option")

    if option == "Planting Calendar":
        st.subheader("🌱 AI-Based Planting Calendar")
        crop = st.text_input("Enter Crop Name:", key="planting_calendar_crop")
        region = st.text_input("Enter Your Region:", key="planting_calendar_region")
        if st.button("Generate Planting Schedule", key="generate_planting_schedule"):
            st.success(f"✅ Recommended planting schedule for {crop.title()} in {region.title()}:")
            st.write("- Best planting month: April")
            st.write("- Expected harvest period: July to August")
            st.write("- Ideal soil moisture: 60%")
            st.write("- AI Tip: Use sensors to monitor rainfall and adjust irrigation.")

    elif option == "Harvest Time Estimator":
        st.subheader("🌾 Harvest Time Estimator")
        crop_type = st.text_input("Enter Crop Type:", key="harvest_crop_type")
        planting_date = st.date_input("Select Planting Date:", key="planting_date")
        if st.button("Estimate Harvest Time", key="estimate_harvest"):
            st.success(f"✅ Estimated harvest time for {crop_type.title()} is 90 days after planting.")
            st.write("📅 Approximate harvest window:", planting_date)
            st.write("🔎 Sensor Alert: Monitor ripeness using image sensors or NDVI analysis.")

    elif option == "Seasonal Task Planner":
        st.subheader("📅 Seasonal Farm Task Planner")
        season = st.selectbox("Select Season", ["Dry Season", "Rainy Season"], key="season_task_planner")
        if st.button("Show Recommended Tasks", key="show_season_tasks"):
            if season == "Rainy Season":
                st.write("- Weed control and disease monitoring")
                st.write("- Fertilizer application planning")
                st.write("- Regular drainage checks")
            else:
                st.write("- land clearing and soil preperation")
                st.Write("- irrigation planning")
                st.write("- AI sensor calibration for dry monitoring")

# 🤖 AI Prediction
elif menu == "🤖 AI Prediction":
    option = st.selectbox("Select Prediction Type", [
        "Crop Disease Detection",
        "Yield Prediction",
        "Soil Health Check"
    ], key="ai_prediction_option")

    if option == "Crop Disease Detection":
        st.subheader("🧪 AI Crop Disease Detection")
        crop = st.text_input("Enter Crop Name:", key="disease_crop_name")
        symptom = st.text_area("Describe Symptoms:", key="disease_symptom_input")
        if st.button("Predict Disease", key="predict_disease_button"):
            # Placeholder AI output
            st.success(f"✅ Predicted disease for {crop.title()}: Leaf Spot Disease")
            st.write("💊 Recommended Treatment: Apply fungicide spray every 7 days for 3 weeks.")
            st.write("🌐 AI Tip: Use smartphone camera or drone to upload plant images in future upgrade.")

    elif option == "Yield Prediction":
        st.subheader("📈 AI Yield Prediction")
        crop = st.text_input("Enter Crop Name:", key="yield_crop_name")
        area = st.number_input("Farm Area (in hectares):", min_value=0.1, step=0.1, key="yield_area_input")
        if st.button("Predict Yield", key="predict_yield_button"):
            st.success(f"✅ Estimated yield for {crop.title()}: {area * 2.5} tons")
            st.write("📊 Based on AI model: avg 2.5 tons/ha under current conditions")
            st.write("📡 Suggestion: Use IoT sensors to monitor soil moisture and adjust fertilization")

    elif option == "Soil Health Check":
        st.subheader("🧬 Soil Health Analysis")

#AI farm tips                         
elif menu == "💡 AI Farm Tips":
    option = st.selectbox("Select an AI Tip Feature", [
        "Ask AI Farm Tip",
        "View Daily Farm Tip"
    ], key="ai_farm_tips_option")

    if option == "Ask AI Farm Tip":
        user_question = st.text_input("Ask a farm-related question:", key="ai_farm_tip_input")
        if st.button("Get AI Tip", key="get_ai_tip_button"):
            if user_question:
                st.write(f"🔍 You asked: {user_question}")
                st.write("💡 AI Tip: (This is where the AI-generated answer will go.)")
            else:
                st.warning("Please enter a question to get an AI tip.")

    elif option == "View Daily Farm Tip":
        st.write("🌱 Tip of the Day: Rotate your crops to improve soil Health and reduce pest.")

# market & economics tools
elif menu == "💹 Market & Economic Tools":
     option = st.selectbox("Select a Market Tool", [
        "Get Market Price",
        "Calculate ROI",
        "Input Cost Estimator"
    ], key="market_tools_option")  # This key is unique for this selectbox   

     if option == "Get Market Price":
          crop_input = st.text_input(
            "Enter crop name to check current market price:", 
            key="market_price_input"
        )
     if st.button("Check Price", key="check_market_price_button"):   
            if crop_input:
                st.success(f"📈 Market Price: The current average market price for {crop_input} is ₦15,000 per 100kg.")
            else:
                st.warning("Please enter a crop name to check the price.")

     elif option == "Calculate ROI":
        investment = st.number_input("Investment (₦):", min_value=0.0, key="roi_investment")
        profit = st.number_input("Expected Profit (₦):", min_value=0.0, key="roi_profit")
        if st.button("Calculate ROI", key="calculate_roi_button"):
            if investment > 0:
                roi = (profit - investment) / investment * 100
                st.success(f"📊 ROI: {roi:.2f}%")
            else:
                st.warning("Investment must be greater than 0.")

     elif option == "Input Cost Estimator":
        seeds = st.number_input("Seed cost (₦):", min_value=0.0, key="input_cost_seeds")
        fertilizer = st.number_input("Fertilizer cost (₦):", min_value=0.0, key="input_cost_fertilizer")
        labor = st.number_input("Labor cost (₦):", min_value=0.0, key="input_cost_labor")
        misc = st.number_input("Other costs (₦):", min_value=0.0, key="input_cost_misc")
        if st.button("Estimate Cost", key="estimate_input_cost_button"):
            total = seeds + fertilizer + las.")p is:", crop)