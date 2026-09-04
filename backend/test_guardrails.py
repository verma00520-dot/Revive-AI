from guardrails import check_action


# ============================================================
# TEST 1 - NORMAL RETRY
# ============================================================

payment = {
    "retry_count": 0,
    "message_count": 0,
    "cancelled": False,
    "opted_out": False
}

result = check_action(
    payment,
    "RETRY_LATER"
)

print("\nTEST 1")
print(result)


# ============================================================
# TEST 2 - MAX RETRIES
# ============================================================

payment = {
    "retry_count": 3,
    "message_count": 0,
    "cancelled": False,
    "opted_out": False
}

result = check_action(
    payment,
    "RETRY_LATER"
)

print("\nTEST 2")
print(result)


# ============================================================
# TEST 3 - CUSTOMER OPTED OUT
# ============================================================

payment = {
    "retry_count": 0,
    "message_count": 0,
    "cancelled": False,
    "opted_out": True
}

result = check_action(
    payment,
    "SEND_REMINDER_AND_RETRY"
)

print("\nTEST 3")
print(result)