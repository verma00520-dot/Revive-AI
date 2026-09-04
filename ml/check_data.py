import pandas as pd

# Load the dataset
df = pd.read_csv("data/payments.csv")

print("=" * 60)
print("           REVIVE AI - DATA INSPECTION")
print("=" * 60)

# 1. Number of rows and columns
print("\n1. DATASET SIZE")
print(f"Rows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")

# 2. Column names
print("\n2. COLUMNS")
for column in df.columns:
    print("-", column)

# 3. First 5 records
print("\n3. FIRST 5 RECORDS")
print(df.head())

# 4. Missing values
print("\n4. MISSING VALUES")
print(df.isnull().sum())

# 5. Data types
print("\n5. DATA TYPES")
print(df.dtypes)

# 6. Recovery distribution
print("\n6. RECOVERY DISTRIBUTION")
print(df["recovered"].value_counts())

# 7. Recovery percentage
recovery_rate = df["recovered"].mean() * 100

print(
    f"\nOverall recovery rate in dataset: "
    f"{recovery_rate:.2f}%"
)

# 8. Failure types
print("\n7. FAILURE TYPES")
print(df["failure_type"].value_counts())

# 9. Payment methods
print("\n8. PAYMENT METHODS")
print(df["payment_method"].value_counts())

# 10. Average payment
print("\n9. PAYMENT AMOUNT")
print(
    f"Average payment: ₹{df['payment_amount'].mean():.2f}"
)

print(
    f"Minimum payment: ₹{df['payment_amount'].min():.2f}"
)

print(
    f"Maximum payment: ₹{df['payment_amount'].max():.2f}"
)

print("\n" + "=" * 60)
print("DATA INSPECTION COMPLETE")
print("=" * 60)