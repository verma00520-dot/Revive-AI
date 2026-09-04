import pandas as pd
import joblib


# ============================================================
# LOAD TRAINED MODEL
# ============================================================

model = joblib.load("models/recovery_model.pkl")


# ============================================================
# CREATE ONE NEW PAYMENT
# ============================================================

new_payment = pd.DataFrame([{
    "payment_amount": 999,
    "failure_type": "insufficient_funds",
    "retry_count": 0,
    "successful_payments": 11,
    "failed_payments": 1,
    "customer_age_days": 320,
    "days_since_failure": 0.5,
    "payment_method": "card",
    "previous_recovery_rate": 0.917
}])


# ============================================================
# PREDICT RECOVERY PROBABILITY
# ============================================================

probability = model.predict_proba(new_payment)[0][1]


# ============================================================
# DISPLAY RESULT
# ============================================================

print("=" * 50)
print("        REVIVE AI - PAYMENT PREDICTION")
print("=" * 50)

print("\nPayment Details:")
print(f"Amount: ₹{new_payment['payment_amount'].iloc[0]}")
print(f"Failure: {new_payment['failure_type'].iloc[0]}")
print(f"Retry count: {new_payment['retry_count'].iloc[0]}")
print(
    f"Successful payments: "
    f"{new_payment['successful_payments'].iloc[0]}"
)
print(
    f"Failed payments: "
    f"{new_payment['failed_payments'].iloc[0]}"
)

print("\n----------------------------------------")

print(
    f"Recovery Probability: "
    f"{probability * 100:.2f}%"
)

print("----------------------------------------")