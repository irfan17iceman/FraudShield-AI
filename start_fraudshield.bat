@echo off
cd /d C:\Fraudshield-AI

echo ========================================
echo       FRAUDSHIELD AI STARTING...
echo ========================================

echo.
echo [1/3] Starting FastAPI...
start "FraudShield - FastAPI" cmd /k "venv\Scripts\activate && uvicorn api:app --reload"

timeout /t 3 /nobreak >nul

echo [2/3] Starting Transaction Simulator...
start "FraudShield - Simulator" cmd /k "venv\Scripts\activate && python simulate_transactions.py"

timeout /t 2 /nobreak >nul

echo [3/3] Starting Streamlit Dashboard...
start "FraudShield - Dashboard" cmd /k "venv\Scripts\activate && python -m streamlit run app.py"

echo.
echo ========================================
echo       FRAUDSHIELD AI IS RUNNING
echo ========================================
echo.
pause