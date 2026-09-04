import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression

import joblib


# ============================================================
# 1. LOAD DATA
# ============================================================

print("=" * 60)
print("           REVIVE AI - MODEL TRAINING")
print("=" * 60)

print("\nLoading dataset...")

df = pd.read_csv("data/payments.csv")

print(f"Dataset loaded successfully.")
print(f"Rows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")


# ============================================================
# 2. REMOVE COLUMNS WE DON'T NEED FOR ML
# ============================================================

# payment_id and customer_id are identifiers.
# They don't provide useful information for our first model.

df = df.drop(
    columns=[
        "payment_id",
        "customer_id"
    ]
)


# ============================================================
# 3. SEPARATE FEATURES (X) AND TARGET (y)
# ============================================================

# Target:
# 1 = payment recovered
# 0 = payment not recovered

X = df.drop(
    columns=["recovered"]
)

y = df["recovered"]


print("\nTarget variable:")
print("recovered")


# ============================================================
# 4. DEFINE FEATURE TYPES
# ============================================================

numeric_features = [
    "payment_amount",
    "retry_count",
    "successful_payments",
    "failed_payments",
    "customer_age_days",
    "days_since_failure",
    "previous_recovery_rate"
]

categorical_features = [
    "failure_type",
    "payment_method"
]


# ============================================================
# 5. PREPROCESSING
# ============================================================

# Convert categorical text into numbers.
# Example:
#
# insufficient_funds
# bank_timeout
# expired_card
#
# become machine-readable columns.

preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(
                handle_unknown="ignore"
            ),
            categorical_features
        ),

        (
            "numeric",
            "passthrough",
            numeric_features
        )
    ]
)


# ============================================================
# 6. CREATE ML PIPELINE
# ============================================================

model = Pipeline(
    steps=[
        (
            "preprocessor",
            preprocessor
        ),

        (
            "classifier",
            LogisticRegression(
                max_iter=1000
            )
        )
    ]
)


# ============================================================
# 7. SPLIT DATA
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


print("\nData split:")
print(f"Training records: {len(X_train)}")
print(f"Testing records: {len(X_test)}")


# ============================================================
# 8. TRAIN MODEL
# ============================================================

print("\nTraining Logistic Regression model...")

model.fit(
    X_train,
    y_train
)

print("Model training completed!")


# ============================================================
# 9. SAVE MODEL
# ============================================================

model_path = "models/recovery_model.pkl"

joblib.dump(
    model,
    model_path
)

print("\nModel saved successfully!")
print(f"Location: {model_path}")


print("\n" + "=" * 60)
print("             TRAINING COMPLETE")
print("=" * 60)