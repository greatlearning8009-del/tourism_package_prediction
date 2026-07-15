# Backend: Flask REST API for the Tourism Package Prediction model
import os
import io
import joblib
import pandas as pd
from flask import Flask, request, jsonify
from huggingface_hub import hf_hub_download

# ------------------------------------------------------------------
# Load the trained model from the Hugging Face MODEL HUB (free tier)
# This is the same repo/file the training step (train.py) pushed to.
# The repo is public, so no token is required to download it.
# ------------------------------------------------------------------
MODEL_REPO_ID = "SRGL/tourism-package-model"
MODEL_FILENAME = "best_tourism_package_model_v1.joblib"

model_path = hf_hub_download(repo_id=MODEL_REPO_ID, filename=MODEL_FILENAME)
model = joblib.load(model_path)

# Classification threshold used during training
CLASSIFICATION_THRESHOLD = 0.45

# Feature order expected by the model pipeline
numeric_features = [
    "Age", "CityTier", "DurationOfPitch", "NumberOfPersonVisiting",
    "NumberOfFollowups", "PreferredPropertyStar", "NumberOfTrips",
    "PitchSatisfactionScore", "NumberOfChildrenVisiting", "MonthlyIncome",
    "Passport", "OwnCar",
]
categorical_features = [
    "TypeofContact", "Occupation", "Gender", "ProductPitched",
    "MaritalStatus", "Designation",
]
FEATURES = numeric_features + categorical_features

app = Flask(__name__)


@app.get("/")
def home():
    return "Tourism Package Prediction API is running. Use POST /v1/predict or /v1/predictbatch."


@app.post("/v1/predict")
def predict():
    # Online (single) inference: expects a JSON object with the feature fields
    data = request.get_json(force=True)
    input_df = pd.DataFrame([data])[FEATURES]

    prob = float(model.predict_proba(input_df)[0, 1])
    pred = int(prob >= CLASSIFICATION_THRESHOLD)
    result = "will purchase the travel package" if pred == 1 else "is unlikely to purchase"

    return jsonify({"prediction": pred, "probability": round(prob, 4), "result": result})


@app.post("/v1/predictbatch")
def predict_batch():
    # Batch inference: expects an uploaded CSV file under the key 'file'
    uploaded = request.files["file"]
    batch_df = pd.read_csv(io.BytesIO(uploaded.read()))

    X = batch_df[FEATURES]
    probs = model.predict_proba(X)[:, 1]
    preds = (probs >= CLASSIFICATION_THRESHOLD).astype(int)

    # Key the output by CustomerID if present, otherwise by row index
    if "CustomerID" in batch_df.columns:
        keys = batch_df["CustomerID"].astype(str).tolist()
    else:
        keys = [str(i) for i in range(len(batch_df))]

    output = {k: int(p) for k, p in zip(keys, preds)}
    return jsonify(output)


if __name__ == "__main__":
    # For local debugging only; in the container gunicorn serves the app
    app.run(host="0.0.0.0", port=7860)
