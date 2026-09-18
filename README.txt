# 🛡️ FraudShield AI

## Real-Time Explainable Financial Fraud Detection

FraudShield AI is a prototype system designed to detect potentially fraudulent financial transactions in real time using Machine Learning.

The system analyzes transaction information, generates a fraud risk score, identifies suspicious indicators, recommends an action, and displays the results through an interactive dashboard.

> **Note:** This is a hackathon prototype that uses synthetic transaction data and a simulated real-time transaction feed. It does not connect to real bank or financial systems.

---

## 🚨 Problem Statement

Financial fraud can cause significant losses when suspicious transactions are not detected quickly.

Traditional rule-based systems may identify certain suspicious patterns, but they may not provide a flexible risk score or clear explanation for every decision.

FraudShield AI aims to provide:

- Real-time transaction monitoring
- Machine-learning-based fraud risk scoring
- Explainable fraud indicators
- Recommended actions
- Interactive monitoring dashboard
- Transaction storage for analysis

---

## 💡 Our Solution

FraudShield AI combines Machine Learning, FastAPI, SQLite, and Streamlit to create an end-to-end fraud detection prototype.

For every incoming transaction, the system:

1. Receives the transaction through the API.
2. Sends relevant transaction features to the trained ML model.
3. Generates a fraud probability.
4. Converts the probability into a risk score from 0–100.
5. Classifies the transaction as LOW, MEDIUM, or HIGH risk.
6. Identifies suspicious indicators.
7. Recommends an action.
8. Stores the transaction and result in SQLite.
9. Displays the result on the Streamlit dashboard.

---

## 🏗️ System Architecture

```text
Transaction Simulator
        ↓
     FastAPI
        ↓
   Fraud Detection
      Model
        ↓
Risk Score + Risk Level
        ↓
Reasons + Recommended Action
        ↓
      SQLite
        ↓
 Streamlit Dashboard