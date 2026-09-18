from fastapi import FastAPI
import joblib
import pandas as pd
import sqlite3
import json

app = FastAPI(title="FraudShield AI API")

# Load ML model
model = joblib.load("fraud_model.pkl")

DB_NAME = "fraudshield.db"


# ---------------- DATABASE ----------------

def init_db():
    conn = sqlite3.connect(DB_NAME)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_id TEXT,
            amount REAL,
            location TEXT,
            device_new INTEGER,
            hour INTEGER,
            velocity INTEGER,
            account_age_days INTEGER,
            risk_score INTEGER,
            risk_level TEXT,
            reasons TEXT,
            recommended_action TEXT
        )
    """)

    conn.commit()
    conn.close()


init_db()


# ---------------- HOME ----------------

@app.get("/")
def home():
    return {
        "message": "FraudShield AI API is running!"
    }


# ---------------- ANALYZE TRANSACTION ----------------

@app.post("/transaction")
def analyze_transaction(transaction: dict):

    # Prepare data for ML model
    data = pd.DataFrame([{
        "amount": transaction["amount"],
        "device_new": transaction["device_new"],
        "hour": transaction["hour"],
        "velocity": transaction["velocity"],
        "account_age_days": transaction["account_age_days"]
    }])

    # ML prediction
    probability = model.predict_proba(data)[0][1]

    risk_score = round(probability * 100)

    # Risk level
    if risk_score >= 70:
        risk_level = "HIGH"
        action = "CHALLENGE"

    elif risk_score >= 40:
        risk_level = "MEDIUM"
        action = "REVIEW"

    else:
        risk_level = "LOW"
        action = "APPROVE"

    # Explainability reasons
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

    # Result
    result = {
        "transaction_id": transaction["transaction_id"],
        "amount": transaction["amount"],
        "location": transaction["location"],
        "risk_score": risk_score,
        "risk_level": risk_level,
        "reasons": reasons,
        "recommended_action": action
    }

    # ---------------- SAVE TO DATABASE ----------------

    conn = sqlite3.connect(DB_NAME)

    conn.execute("""
        INSERT INTO transactions (
            transaction_id,
            amount,
            location,
            device_new,
            hour,
            velocity,
            account_age_days,
            risk_score,
            risk_level,
            reasons,
            recommended_action
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        transaction["transaction_id"],
        transaction["amount"],
        transaction["location"],
        transaction["device_new"],
        transaction["hour"],
        transaction["velocity"],
        transaction["account_age_days"],
        risk_score,
        risk_level,
        json.dumps(reasons),
        action
    ))

    conn.commit()
    conn.close()

    return result


# ---------------- GET TRANSACTIONS ----------------

@app.get("/transactions")
def get_transactions():

    conn = sqlite3.connect(DB_NAME)

    df = pd.read_sql_query(
        "SELECT * FROM transactions ORDER BY id DESC",
        conn
    )

    conn.close()

    return df.to_dict(orient="records")