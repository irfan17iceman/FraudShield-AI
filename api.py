from fastapi import FastAPI
import joblib
import pandas as pd

app = FastAPI(title="FraudShield AI API")

# Load trained model
model = joblib.load("fraud_model.pkl")


@app.get("/")
def home():
    return {
        "message": "FraudShield AI API is running!"
    }


@app.post("/transaction")
def analyze_transaction(transaction: dict):

    # Prepare transaction for the model
    data = pd.DataFrame([{
        "amount": transaction["amount"],
        "device_new": transaction["device_new"],
        "hour": transaction["hour"],
        "velocity": transaction["velocity"],
        "account_age_days": transaction["account_age_days"]
    }])

    # Get fraud probability
    probability = model.predict_proba(data)[0][1]

    # Convert to percentage
    risk_score = round(probability * 100)

    # Determine risk level
    if risk_score >= 70:
        risk_level = "HIGH"
        action = "CHALLENGE"
    elif risk_score >= 40:
        risk_level = "MEDIUM"
        action = "REVIEW"
    else:
        risk_level = "LOW"
        action = "APPROVE"

    # Generate explanations
    reasons = []

    if transaction["amount"] >= 30000:
        reasons.append("High transaction amount")

    if transaction["device_new"] == 1:
        reasons.append("New device detected")

    if transaction["hour"] <= 4:
        reasons.append("Unusual transaction time")

    if transaction["velocity"] >= 5:
        reasons.append("High transaction velocity")

    if transaction["account_age_days"] < 100:
        reasons.append("New account")

    if not reasons:
        reasons.append("No major suspicious indicators detected")

    return {
        "transaction_id": transaction["transaction_id"],
        "risk_score": risk_score,
        "risk_level": risk_level,
        "reasons": reasons,
        "recommended_action": action
    }