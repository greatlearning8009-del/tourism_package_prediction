import streamlit as st
import pandas as pd
import requests

# Base URL of the Flask backend on the shared Docker network
BACKEND_URL = "http://backend:7860"

st.title("Tourism Package Prediction")
st.write("Fill the customer details below to predict if they'll purchase a travel package")

# ---------------- Online (single) prediction ----------------
st.header("Single prediction")

Age = st.slider("Age", 18, 70, 30)
TypeofContact = st.selectbox("Type of Contact", ["Self Enquiry", "Company Invited"])
CityTier = st.selectbox("City Tier", [1, 2, 3])
DurationOfPitch = st.slider("Duration of Pitch (mins)", 0, 100, 15)
Occupation = st.selectbox("Occupation", ["Salaried", "Small Business", "Large Business", "Free Lancer"])
Gender = st.selectbox("Gender", ["Male", "Female", "Others"])
NumberOfPersonVisiting = st.slider("Number of Persons Visiting", 1, 5, 2)
NumberOfFollowups = st.slider("Number of Follow-ups", 1, 10, 3)
ProductPitched = st.selectbox("Product Pitched", ["Basic", "Standard", "Deluxe", "Super Deluxe", "King"])
PreferredPropertyStar = st.selectbox("Preferred Property Star", [1, 2, 3, 4, 5])
MaritalStatus = st.selectbox("Marital Status", ["Married", "Single", "Divorced", "Unmarried"])
NumberOfTrips = st.slider("Number of Trips", 1, 20, 3)
Passport = st.selectbox("Has Passport?", ["Yes", "No"])
PitchSatisfactionScore = st.slider("Pitch Satisfaction Score", 1, 5, 3)
OwnCar = st.selectbox("Owns a Car?", ["Yes", "No"])
NumberOfChildrenVisiting = st.slider("Number of Children Visited", 0, 5, 1)
Designation = st.selectbox("Designation", ["Executive", "Manager", "AVP", "VP", "Sr. Manager"])
MonthlyIncome = st.number_input("Monthly Income", min_value=1000.0, value=30000.0)

payload = {
    "Age": Age,
    "TypeofContact": TypeofContact,
    "CityTier": CityTier,
    "DurationOfPitch": DurationOfPitch,
    "Occupation": Occupation,
    "Gender": Gender,
    "NumberOfPersonVisiting": NumberOfPersonVisiting,
    "NumberOfFollowups": NumberOfFollowups,
    "ProductPitched": ProductPitched,
    "PreferredPropertyStar": PreferredPropertyStar,
    "MaritalStatus": MaritalStatus,
    "NumberOfTrips": NumberOfTrips,
    "Passport": 1 if Passport == "Yes" else 0,
    "PitchSatisfactionScore": PitchSatisfactionScore,
    "OwnCar": 1 if OwnCar == "Yes" else 0,
    "NumberOfChildrenVisiting": NumberOfChildrenVisiting,
    "Designation": Designation,
    "MonthlyIncome": MonthlyIncome,
}

if st.button("Predict"):
    try:
        response = requests.post(f"{BACKEND_URL}/v1/predict", json=payload)
        response.raise_for_status()
        out = response.json()
        st.success(f"Prediction: Customer {out['result']} (probability {out['probability']})")
    except Exception as e:
        st.error(f"Could not reach backend: {e}")

# ---------------- Batch prediction ----------------
st.header("Batch prediction")
st.write("Upload a CSV with the customer feature columns to score many rows at once.")

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
if st.button("Predict Batch"):
    if uploaded_file is None:
        st.warning("Please upload a CSV file first.")
    else:
        try:
            files = {"file": ("batch.csv", uploaded_file.getvalue(), "text/csv")}
            response = requests.post(f"{BACKEND_URL}/v1/predictbatch", files=files)
            response.raise_for_status()
            results = response.json()
            st.write("Predictions (1 = will purchase, 0 = unlikely):")
            st.json(results)
        except Exception as e:
            st.error(f"Could not reach backend: {e}")
