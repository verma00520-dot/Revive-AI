import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)


# ============================================================
# LOAD DATA
# ============================================================

df = pd.read_csv("data/payments.csv")


# ============================================================
# PREPARE DATA
# ============================================================

X = df.drop(
    columns=[
        "recovered",
        "payment_id",
        "customer_id"
    ]
)

y = df["recovered"]


# ============================================================
# TRAIN / TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# ============================================================
# LOAD TRAINED MODEL
# ============================================================

model = joblib.load(
    "models/recovery_model.pkl"
)


# ============================================================
# MAKE PREDICTIONS
# ============================================================

predictions = model.predict(X_test)

probabilities = model.predict_proba(
    X_test
)[:, 1]


# ============================================================
# CALCULATE METRICS
# ============================================================

accuracy = accuracy_score(
    y_test,
    predictions
)

precision = precision_score(
    y_test,
    predictions
)

recall = recall_score(
    y_test,
    predictions
)

f1 = f1_score(
    y_test,
    predictions
)

roc_auc = roc_auc_score(
    y_test,
    probabilities
)


# ============================================================
# DISPLAY RESULTS
# ============================================================

print("=" * 60)
print("          REVIVE AI - MODEL EVALUATION")
print("=" * 60)

print(f"\nAccuracy : {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall   : {recall:.4f}")
print(f"F1 Score : {f1:.4f}")
print(f"ROC-AUC  : {roc_auc:.4f}")


print("\nClassification Report:")
print(
    classification_report(
        y_test,
        predictions
    )
)


print("\nConfusion Matrix:")
print(
    confusion_matrix(
        y_test,
        predictions
    )
)

print("\n" + "=" * 60)
print("          EVALUATION COMPLETE")
print("=" * 60)