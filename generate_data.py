import pandas as pd
import random

random.seed(42)

transactions = []

for i in range(1000):

    # Decide whether this transaction is normal or suspicious
    is_fraud = random.random() < 0.20

    if is_fraud:
        amount = random.randint(30000, 150000)
        device_new = 1
        hour = random.choice([0, 1, 2, 3, 4])
        velocity = random.randint(5, 15)
        account_age_days = random.randint(5, 100)
        location = random.choice([
            "Delhi",
            "Mumbai",
            "Bangalore",
            "Hyderabad"
        ])
    else:
        amount = random.randint(100, 15000)
        device_new = random.choice([0, 0, 0, 1])
        hour = random.randint(7, 22)
        velocity = random.randint(1, 4)
        account_age_days = random.randint(100, 2000)
        location = random.choice([
            "Chennai",
            "Coimbatore",
            "Madurai",
            "Salem"
        ])

    transactions.append({
        "transaction_id": f"TXN{i+1:04d}",
        "amount": amount,
        "location": location,
        "device_new": device_new,
        "hour": hour,
        "velocity": velocity,
        "account_age_days": account_age_days,
        "is_fraud": is_fraud
    })

df = pd.DataFrame(transactions)

df.to_csv("transactions.csv", index=False)

print("Dataset created successfully!")
print(f"Total transactions: {len(df)}")
print(f"Fraud transactions: {df['is_fraud'].sum()}")
print(f"Normal transactions: {(~df['is_fraud']).sum()}")