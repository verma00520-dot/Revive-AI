import pandas as pd
import numpy as np
import random

# ============================================================
# REVIVE AI - SYNTHETIC SUBSCRIPTION PAYMENT DATA GENERATOR
# ============================================================

# Number of payment records we want to create
NUM_RECORDS = 8000

# Keep results reproducible
random.seed(42)
np.random.seed(42)


# ============================================================
# POSSIBLE FAILURE TYPES
# ============================================================

failure_types = [
    "insufficient_funds",
    "bank_timeout",
    "expired_card",
    "invalid_card",
    "authentication_failed"
]


# ============================================================
# POSSIBLE PAYMENT METHODS
# ============================================================

payment_methods = [
    "card",
    "upi",
    "netbanking"
]


# ============================================================
# GENERATE PAYMENT DATA
# ============================================================

data = []

for i in range(NUM_RECORDS):

    # ----------------------------
    # Basic payment information
    # ----------------------------

    payment_id = f"pay_{i + 1:05d}"

    customer_id = f"cust_{random.randint(1, 2500):04d}"

    # Generate realistic subscription amounts
    payment_amount = round(
        random.choice([
            random.uniform(199, 499),
            random.uniform(500, 999),
            random.uniform(1000, 2999),
            random.uniform(3000, 9999)
        ]),
        2
    )

    failure_type = random.choice(failure_types)

    payment_method = random.choice(payment_methods)

    # Number of previous retry attempts
    retry_count = random.randint(0, 3)

    # Customer payment history
    successful_payments = random.randint(0, 20)

    failed_payments = random.randint(0, 8)

    # How long customer has been subscribed
    customer_age_days = random.randint(30, 1000)

    # How long ago the payment failed
    days_since_failure = round(
        random.uniform(0.1, 5.0),
        2
    )

    # ========================================================
    # PREVIOUS RECOVERY RATE
    # ========================================================

    total_previous_payments = (
        successful_payments + failed_payments
    )

    if total_previous_payments > 0:
        previous_recovery_rate = (
            successful_payments / total_previous_payments
        )
    else:
        previous_recovery_rate = 0.0


    # ========================================================
    # CREATE A REALISTIC RECOVERY PROBABILITY
    # ========================================================

    probability = 0.50


    # Strong customer payment history
    if successful_payments >= 10:
        probability += 0.15

    elif successful_payments >= 5:
        probability += 0.08


    # Too many previous failures
    if failed_payments >= 5:
        probability -= 0.15

    elif failed_payments >= 3:
        probability -= 0.08


    # Too many retries
    if retry_count == 1:
        probability -= 0.03

    elif retry_count == 2:
        probability -= 0.12

    elif retry_count >= 3:
        probability -= 0.25


    # ========================================================
    # FAILURE-SPECIFIC BEHAVIOR
    # ========================================================

    if failure_type == "bank_timeout":

        # Temporary bank issue
        probability += 0.18

    elif failure_type == "insufficient_funds":

        # Can potentially recover later
        probability += 0.08

    elif failure_type == "expired_card":

        # Payment method needs attention
        probability -= 0.10

    elif failure_type == "invalid_card":

        # Less likely to recover by simple retry
        probability -= 0.18

    elif failure_type == "authentication_failed":

        probability -= 0.08


    # ========================================================
    # HISTORICAL RECOVERY RATE
    # ========================================================

    if previous_recovery_rate >= 0.80:

        probability += 0.10

    elif previous_recovery_rate >= 0.60:

        probability += 0.05

    elif previous_recovery_rate < 0.30:

        probability -= 0.10


    # ========================================================
    # ADD SMALL RANDOMNESS
    # ========================================================

    probability += np.random.normal(0, 0.05)


    # Keep probability between 0.02 and 0.98
    probability = max(
        0.02,
        min(0.98, probability)
    )


    # ========================================================
    # CREATE ACTUAL RECOVERY OUTCOME
    # ========================================================

    # 1 = recovered
    # 0 = not recovered

    recovered = np.random.binomial(
        1,
        probability
    )


    # ========================================================
    # SAVE RECORD
    # ========================================================

    data.append({

        "payment_id": payment_id,

        "customer_id": customer_id,

        "payment_amount": round(
            payment_amount,
            2
        ),

        "failure_type": failure_type,

        "retry_count": retry_count,

        "successful_payments": successful_payments,

        "failed_payments": failed_payments,

        "customer_age_days": customer_age_days,

        "days_since_failure": days_since_failure,

        "payment_method": payment_method,

        "previous_recovery_rate": round(
            previous_recovery_rate,
            3
        ),

        "recovered": recovered
    })


# ============================================================
# CREATE DATAFRAME
# ============================================================

df = pd.DataFrame(data)


# ============================================================
# SAVE DATASET
# ============================================================

output_path = "data/payments.csv"

df.to_csv(
    output_path,
    index=False
)


# ============================================================
# DISPLAY RESULTS
# ============================================================

print()
print("=" * 60)
print("        REVIVE AI - DATA GENERATION")
print("=" * 60)

print()
print(f"Total records generated: {len(df)}")

print()
print("Recovery distribution:")
print(
    df["recovered"]
    .value_counts()
    .rename({
        0: "Not Recovered",
        1: "Recovered"
    })
)

print()
print("Failure type distribution:")
print(
    df["failure_type"].value_counts()
)

print()
print("Payment method distribution:")
print(
    df["payment_method"].value_counts()
)

print()
print("Average payment amount:")
print(
    f"₹{df['payment_amount'].mean():.2f}"
)

print()
print("Dataset saved to:")
print(output_path)

print()
print("=" * 60)