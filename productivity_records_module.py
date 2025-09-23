import streamlit as st

st.set_page_config(page_title="Test", layout="wide")

menu = st.sidebar.selectbox("📖 Main Menu", [
    "🏡 Home",
    "📊 Productivity & Records"
])

if menu == "🏡 Home":
    st.subheader("Welcome!")

elif menu == "📊 Productivity & Records":
    option = st.selectbox("Select a Feature", [
        "View Sales Record",
        "View Expense",
        "Calculate Profit"
    ], key="productivity")

    if option == "View Sales Record":
        st.subheader("View Sales Record")
        crop = st.text_input("Crop Name:")
        quantity = st.number_input("Quantity Sold (kg):", min_value=0)
        if st.button("Save"):
            st.success(f"Saved {quantity} kg of {crop}")

    elif option == "View Expense":
        st.subheader("View Expense")
        expense = st.text_input("Expense Name:")
        amount = st.number_input("Amount (₦):", min_value=0)
        if st.button("Log Expense"):
            st.success(f"Logged {expense} - ₦{amount}")

    elif option == "Calculate Profit":
        st.subheader("Calculate Profit")
        sales = st.number_input("Total Sales (₦):", min_value=0)
        expenses = st.number_input("Total Expenses (₦):", min_value=0)
        if st.button("Calculate"):
            st.success(f"Profit: ₦{sales - expenses}")