import streamlit as st

st.title("🌱 Smart Farm AI - Fertilizer Recommendation System")

# Crop selection
crop = st.selectbox("Select Crop", ["Maize", "Rice", "Tomato", "Cassava", "Yam"])

# Season selection
season = st.selectbox("Select Season", ["Rainy", "Dry"])

# Soil type selection
soil = st.selectbox("Select Soil Type", ["Loamy", "Clay", "Sandy", "Silty"])

# Recommendation logic
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

    # Additional advice based on season and soil
    if season == "Rainy" and soil in ["Clay", "Silty"]:
        st.warning("⚠️ Ensure proper drainage to avoid waterlogging.")