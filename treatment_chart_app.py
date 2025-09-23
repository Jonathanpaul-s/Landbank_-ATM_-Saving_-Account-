import streamlit as st
import matplotlib.pyplot as plt

# Sample data: Disease and list of treatments
treatment_data = {
    "Leaf Spot": ["Fungicide A", "Prune Leaves", "Use Clean Tools"],
    "Rust": ["Fungicide B", "Crop Rotation"],
    "Blight": ["Fungicide C", "Remove Infected Plants", "Improve Drainage"],
    "Powdery Mildew": ["Fungicide D", "Increase Air Circulation"],
    "Wilt": ["Soil Treatment", "Resistant Varieties", "Proper Irrigation"]
}

# Count the number of treatments per disease
diseases = list(treatment_data.keys())
treatment_counts = [len(treatments) for treatments in treatment_data.values()]

# Streamlit app layout
st.set_page_config(page_title="Treatments Chart", layout="centered")
st.title("📊 Treatments per Disease")
st.write("This chart shows how many treatment methods are recommended for each crop disease.")

# Create bar chart
fig, ax = plt.subplots()
ax.bar(diseases, treatment_counts, color='green')
ax.set_ylabel("Number of Treatments")
ax.set_xlabel("Disease")
ax.set_title("Number of Treatments per Disease")
plt.xticks(rotation=45)

# Display the chart
st.pyplot(fig)

# Optional: Show full treatment list below
with st.expander("🔍 View Treatments for Each Disease"):
    for disease, treatments in treatment_data.items():
        st.markdown(f"**{disease}**:")
        for t in treatments:
            st.markdown(f"- {t}")