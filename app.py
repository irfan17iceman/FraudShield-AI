import streamlit as st
import requests
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
import time

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="FraudShield AI",
    page_icon="🛡️",
    layout="wide"
)

API_URL = "http://127.0.0.1:8000"

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("🛡️ FraudShield AI")
st.subheader("Real-Time Explainable Financial Fraud Detection")

st.markdown(
    "Live transactions are received from the simulator through FastAPI "
    "and analyzed using the fraud detection model."
)

# --------------------------------------------------
# GET DATA FROM FASTAPI
# --------------------------------------------------

def get_transactions():

    try:
        response = requests.get(
            f"{API_URL}/transactions",
            timeout=5
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.ConnectionError:
        st.error(
            "❌ FastAPI is not running. "
            "Start it using: uvicorn api:app --reload"
        )
        return []

    except Exception as e:
        st.error(f"❌ Could not get transactions: {e}")
        return []


transactions = get_transactions()

# --------------------------------------------------
# MAIN DASHBOARD
# --------------------------------------------------

if transactions:

    df = pd.DataFrame(transactions)

    # Make sure newest transaction appears first
    if "id" in df.columns:
        df = df.sort_values("id", ascending=False)

    # --------------------------------------------------
    # METRICS
    # --------------------------------------------------

    total = len(df)

    high = len(
        df[df["risk_level"] == "HIGH"]
    )

    medium = len(
        df[df["risk_level"] == "MEDIUM"]
    )

    low = len(
        df[df["risk_level"] == "LOW"]
    )

    avg_score = round(df["risk_score"].mean(), 1)

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric(
        "Total Transactions",
        total
    )

    col2.metric(
        "🔴 High Risk",
        high
    )

    col3.metric(
        "🟠 Medium Risk",
        medium
    )

    col4.metric(
        "🟢 Low Risk",
        low
    )

    col5.metric(
        "Average Risk Score",
        avg_score
    )

    st.divider()

    # --------------------------------------------------
    # LATEST TRANSACTION
    # --------------------------------------------------

    st.subheader("🚨 Latest Transaction")

    latest = df.iloc[0]

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Transaction ID",
        latest["transaction_id"]
    )

    col2.metric(
        "Amount",
        f"₹{latest['amount']:,.0f}"
    )

    col3.metric(
        "Risk Score",
        latest["risk_score"]
    )

    col4.metric(
        "Risk Level",
        latest["risk_level"]
    )

    st.write(
        "**Location:**",
        latest["location"]
    )

    st.write(
        "**Recommended Action:**",
        latest["recommended_action"]
    )

    # --------------------------------------------------
    # FRAUD REASONS
    # --------------------------------------------------

    st.write("### 🔍 Fraud Reasons")

    reasons = latest["reasons"]

    if isinstance(reasons, str):
        try:
            reasons = json.loads(reasons)
        except:
            reasons = [reasons]

    if reasons:

        for reason in reasons:
            st.write(f"• {reason}")

    st.divider()

    # --------------------------------------------------
    # RISK DISTRIBUTION
    # --------------------------------------------------

    st.subheader("📊 Risk Distribution")

    risk_counts = (
        df["risk_level"]
        .value_counts()
        .reset_index()
    )

    risk_counts.columns = [
        "Risk Level",
        "Count"
    ]

    fig_pie = px.pie(
        risk_counts,
        names="Risk Level",
        values="Count",
        title="Transaction Risk Distribution",
        hole=0.4
    )

    st.plotly_chart(
        fig_pie,
        use_container_width=True
    )

    # --------------------------------------------------
    # RISK SCORE CHART
    # --------------------------------------------------

    st.subheader("📈 Risk Score Over Transactions")

    chart_df = df.sort_values("id")

    fig_line = px.line(
        chart_df,
        x="transaction_id",
        y="risk_score",
        markers=True,
        title="Real-Time Fraud Risk Score"
    )

    fig_line.add_hline(
        y=70,
        line_dash="dash",
        annotation_text="High Risk Threshold"
    )

    fig_line.add_hline(
        y=40,
        line_dash="dash",
        annotation_text="Medium Risk Threshold"
    )

    fig_line.update_yaxes(
        range=[0, 100]
    )

    st.plotly_chart(
        fig_line,
        use_container_width=True
    )

    # --------------------------------------------------
    # TRANSACTION AMOUNT CHART
    # --------------------------------------------------

    st.subheader("💰 Transaction Amount Analysis")

    fig_amount = px.bar(
        chart_df.tail(20),
        x="transaction_id",
        y="amount",
        title="Latest 20 Transaction Amounts",
        hover_data=[
            "location",
            "risk_score",
            "risk_level"
        ]
    )

    st.plotly_chart(
        fig_amount,
        use_container_width=True
    )

    # --------------------------------------------------
    # RISK LEVEL BAR CHART
    # --------------------------------------------------

    st.subheader("🚦 Risk Level Summary")

    fig_bar = px.bar(
        risk_counts,
        x="Risk Level",
        y="Count",
        text="Count",
        title="Number of Transactions by Risk Level"
    )

    fig_bar.update_traces(
        textposition="outside"
    )

    st.plotly_chart(
        fig_bar,
        use_container_width=True
    )

    # --------------------------------------------------
    # RECENT TRANSACTIONS TABLE
    # --------------------------------------------------

    st.subheader("📋 Recent Transactions")

    display_columns = [
        "transaction_id",
        "amount",
        "location",
        "risk_score",
        "risk_level",
        "recommended_action"
    ]

    available_columns = [
        col for col in display_columns
        if col in df.columns
    ]

    st.dataframe(
        df[available_columns].head(20),
        use_container_width=True,
        hide_index=True
    )

    # --------------------------------------------------
    # TRANSACTION DETAILS
    # --------------------------------------------------

    with st.expander("🔎 View Transaction Details"):

        st.dataframe(
            df.head(20),
            use_container_width=True,
            hide_index=True
        )

else:

    st.warning(
        "⏳ Waiting for transactions from the simulator..."
    )

# --------------------------------------------------
# AUTO REFRESH
# --------------------------------------------------

time.sleep(5)
st.rerun()