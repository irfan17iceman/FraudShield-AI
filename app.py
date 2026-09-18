import streamlit as st
import pandas as pd
import requests
import time

st.set_page_config(
    page_title="FraudShield AI",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ FraudShield AI")
st.subheader("Real-Time Fraud Detection Dashboard")

API_URL = "http://127.0.0.1:8000/transaction"

st.write("Click the button below to generate and analyze a transaction.")

if st.button("🚀 Analyze New Transaction"):

    import random

    transaction = {
        "transaction_id": f"WEB{random.randint(1000, 9999)}",
        "amount": random.randint(500, 100000),
        "location": random.choice([
            "Chennai",
            "Coimbatore",
            "Madurai",
            "Mumbai",
            "Delhi",
            "Bangalore"
        ]),
        "device_new": random.choice([0, 0, 0, 1]),
        "hour": random.randint(0, 23),
        "velocity": random.randint(1, 12),
        "account_age_days": random.randint(10, 2000)
    }

    try:
        response = requests.post(
            API_URL,
            json=transaction,
            timeout=5
        )

        result = response.json()

        st.write("### Transaction")
        st.json(transaction)

        st.write("### Fraud Analysis")

        col1, col2, col3 = st.columns(3)

        col1.metric("Risk Score", result["risk_score"])
        col2.metric("Risk Level", result["risk_level"])
        col3.metric("Action", result["recommended_action"])

        st.write("### 🚨 Reasons")

        for reason in result["reasons"]:
            st.write("•", reason)

    except Exception as e:
        st.error(f"Could not connect to API: {e}")