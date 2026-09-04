from decision_engine import choose_action


print("=" * 60)
print("       REVIVE AI - DECISION ENGINE TEST")
print("=" * 60)


# ============================================================
# TEST 1 - INSUFFICIENT FUNDS
# ============================================================

print("\n\nTEST 1: INSUFFICIENT FUNDS")

failure_type = "insufficient_funds"
recovery_probability = 0.84
retry_count = 0
successful_payments = 11
failed_payments = 1

result = choose_action(
    failure_type=failure_type,
    recovery_probability=recovery_probability,
    retry_count=retry_count,
    successful_payments=successful_payments,
    failed_payments=failed_payments
)

print("Failure Type:", failure_type)
print("Recovery Probability:", f"{recovery_probability * 100:.0f}%")
print("AI Decision:", result["action"])
print("Reason:", result["reason"])


# ============================================================
# TEST 2 - EXPIRED CARD
# ============================================================

print("\n\nTEST 2: EXPIRED CARD")

failure_type = "expired_card"
recovery_probability = 0.84
retry_count = 0
successful_payments = 11
failed_payments = 1

result = choose_action(
    failure_type=failure_type,
    recovery_probability=recovery_probability,
    retry_count=retry_count,
    successful_payments=successful_payments,
    failed_payments=failed_payments
)

print("Failure Type:", failure_type)
print("Recovery Probability:", f"{recovery_probability * 100:.0f}%")
print("AI Decision:", result["action"])
print("Reason:", result["reason"])


# ============================================================
# TEST 3 - BANK TIMEOUT
# ============================================================

print("\n\nTEST 3: BANK TIMEOUT")

failure_type = "bank_timeout"
recovery_probability = 0.88
retry_count = 0
successful_payments = 9
failed_payments = 1

result = choose_action(
    failure_type=failure_type,
    recovery_probability=recovery_probability,
    retry_count=retry_count,
    successful_payments=successful_payments,
    failed_payments=failed_payments
)

print("Failure Type:", failure_type)
print("Recovery Probability:", f"{recovery_probability * 100:.0f}%")
print("AI Decision:", result["action"])
print("Reason:", result["reason"])


# ============================================================
# TEST 4 - MAX RETRIES
# ============================================================

print("\n\nTEST 4: MAXIMUM RETRIES")

failure_type = "insufficient_funds"
recovery_probability = 0.90
retry_count = 3
successful_payments = 10
failed_payments = 2

result = choose_action(
    failure_type=failure_type,
    recovery_probability=recovery_probability,
    retry_count=retry_count,
    successful_payments=successful_payments,
    failed_payments=failed_payments
)

print("Failure Type:", failure_type)
print("Recovery Probability:", f"{recovery_probability * 100:.0f}%")
print("Retry Count:", retry_count)
print("AI Decision:", result["action"])
print("Reason:", result["reason"])


print("\n" + "=" * 60)
print("             ALL TESTS COMPLETED")
print("=" * 60)