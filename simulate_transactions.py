import random
import time
import requests

API_URL = "http://127.0.0.1:8000/transaction"

locations = [
    "Chennai",
    "Coimbatore",
    "Madurai",
    "Mumbai",
    "Delhi",
    "Bangalore"
]

transaction_number = 1

while True:

    transaction = {
        "transaction_id": f"LIVE{transaction_number:04d}",
        "amount": random.randint(500, 100000),
        "location": random.choice(locations),
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

        print("\nNEW TRANSACTION")
        print(transaction)

        print("API RESPONSE")
        print(response.json())
        result = response.json()

        if result["risk_level"] == "HIGH":
            print("🚨 FRAUD DETECTED!")
            print("🛑 TRANSACTION BLOCKED!")
        else:
            print("✅ TRANSACTION ALLOWED")

    except Exception as e:
        print("Could not connect to API:", e)

    transaction_number += 1

    time.sleep(5)