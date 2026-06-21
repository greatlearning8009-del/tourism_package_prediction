import streamlit as st
import pandas as pd
from huggingface_hub import hf_hub_download
import joblib

# Download and load the model
model_path = hf_hub_download(repo_id="pratikshadhumal12/tourism_package_prediction_model", filename="best_tourism_package_prediction_model_v1.joblib")
model = joblib.load(model_path)

# Streamlit UI for Machine Failure Prediction
st.title("Wellness Tourism Package Prediction App")
st.write("""
This application predicts the likelihood of a tourism package based on its operational parameters.
Please enter the data below to get a prediction.
""")

# User input
Age = st.number_input("Age", min_value=18, max_value=100, value=30)
TypeofContact = st.selectbox("Type of Contact", ["Company Invited", "Self Enquiry"])
CityTier = st.selectbox("City Tier", [1,2,3])
DurationOfPitch = st.number_input("Duration of Pitch", min_value=1, max_value=127, value=50)
Occupation = st.selectbox("Occupation", ['Salaried', 'Small Business', 'Large Business', 'Free Lancer'])
Gender = st.selectbox("Gender", ["Female", "Male"])
NumberOfPersonVisiting = st.number_input("Number of Person Visiting", min_value=1, max_value=10, value=2)
NumberOfFollowups = st.number_input("Number of Followups", min_value=0, max_value=10, value=2)
PreferredPropertyStar = st.selectbox("Preferred Property Star", [1,2,3,4,5])
NumberOfTrips = st.number_input("Number of Trips", min_value=0, max_value=60, value=2)
Passport = st.selectbox("Passport", ["Yes", "No"])
PitchSatisfactionScore = st.slider("Pitch Satisfaction Score", min_value=1, max_value=10, value=5)
OwnCar = st.selectbox("Own Car", ["Yes", "No"])
NumberOfChildrenVisiting = st.number_input("Number of Children Visiting", min_value=0, max_value=10, value=2)
MonthlyIncome = st.number_input("Monthly Income", min_value=1000, max_value=100000, value=10000)
ProductPitched = st.selectbox("Product Pitched", ["Basic", "Standard", "Deluxe", "Super Deluxe","King"])
MaritalStatus = st.selectbox("Marital Status", ["Single", "Married", "Divorced"])
Designation = st.selectbox("Designation", ["Executive", "Manager", "Senior Manager", "VP", "AVP"])


# Assemble input into DataFrame
input_data = pd.DataFrame([{
    "Age": Age,
    "TypeofContact": TypeofContact,
    "CityTier": CityTier,
    "DurationOfPitch": DurationOfPitch,
    "Occupation": Occupation,
    "Gender": Gender,
    "NumberOfPersonVisiting": NumberOfPersonVisiting,
    "NumberOfFollowups": NumberOfFollowups,
    "PreferredPropertyStar": PreferredPropertyStar,
    "NumberOfTrips": NumberOfTrips,
    "Passport": Passport,
    "PitchSatisfactionScore": PitchSatisfactionScore,
    "OwnCar": OwnCar,
    "NumberOfChildrenVisiting": NumberOfChildrenVisiting,
    "MonthlyIncome": MonthlyIncome,
    "ProductPitched": ProductPitched,
    "MaritalStatus": MaritalStatus,
    "Designation": Designation

}])

if st.button("Predict"):
    prediction_proba = model.predict_proba(input_data)[0, 1]
    prediction = (prediction_proba >= classification_threshold).astype(int)


    if prediction == 1:
        st.success("The customer is likely to purchase the package.")
    else:
        st.error("The customer is unlikely to purchase the package.")
