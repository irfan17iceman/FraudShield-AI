import streamlit as st

st.set_page_config(
    page_title="FraudShield AI",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ FraudShield AI")
st.subheader("Explainable Financial Fraud Detection")

st.write(
    "Analyze a transaction and identify potentially suspicious activity."
)

st.divider()

st.header("Transaction Details")

col1, col2 = st.columns(2)

with col1:
    transaction_id = st.text_input(
        "Transaction ID",
        value="TXN-1001"
    )

    amount = st.number_input(
        "Transaction Amount (₹)",
        min_value=0.0,
        value=5000.0,
        step=500.0
    )

    location = st.text_input(
        "Location",
        value="Chennai"
    )

with col2:
    device_id = st.text_input(
        "Device ID",
        value="DEVICE-001"
    )

    merchant_id = st.text_input(
        "Merchant ID",
        value="MERCHANT-001"
    )

    transaction_time = st.time_input(
        "Transaction Time"
    )

st.divider()

if st.button("🔍 Analyze Transaction", type="primary"):

    st.success("Transaction received successfully!")

    st.subheader("Transaction Summary")

    st.write(f"**Transaction ID:** {transaction_id}")
    st.write(f"**Amount:** ₹{amount:,.2f}")
    st.write(f"**Location:** {location}")
    st.write(f"**Device:** {device_id}")
    st.write(f"**Merchant:** {merchant_id}")
    st.write(f"**Time:** {transaction_time}")

    st.info(
        "The fraud detection model will be connected here."
    )