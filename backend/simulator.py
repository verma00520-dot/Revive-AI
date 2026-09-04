# ============================================================
# REVIVE AI - RECOVERY SIMULATOR
# ============================================================

def simulate_retry(payment, recovery_probability):
    """
    Simulates a payment retry.

    For the hackathon demo, we use a deterministic result
    based on the payment's simulated outcome.

    This does NOT move real money.
    """

    # If this flag exists, use it.
    if "simulated_retry_success" in payment:

        if payment["simulated_retry_success"]:
            return {
                "status": "SUCCESS",
                "recovered_amount": payment["payment_amount"]
            }

        return {
            "status": "FAILED",
            "recovered_amount": 0
        }

    # Fallback behaviour
    return {
        "status": "FAILED",
        "recovered_amount": 0
    }


# ============================================================
# CUSTOMER MESSAGE SIMULATOR
# ============================================================

def simulate_message(payment):

    customer_name = payment.get(
        "customer_name",
        "Customer"
    )

    amount = payment["payment_amount"]

    if payment["failure_type"] == "expired_card":

        message = (
            f"Hi {customer_name}, your subscription payment "
            f"of ₹{amount:.2f} could not be completed because "
            f"your saved payment method needs to be updated."
        )

    elif payment["failure_type"] == "insufficient_funds":

        message = (
            f"Hi {customer_name}, we could not complete your "
            f"subscription payment of ₹{amount:.2f}. "
            f"We will try again later. Please make sure "
            f"sufficient funds are available."
        )

    elif payment["failure_type"] == "bank_timeout":

        message = (
            f"Hi {customer_name}, we could not complete your "
            f"subscription payment of ₹{amount:.2f} because "
            f"of a temporary bank issue. We will try again later."
        )

    else:

        message = (
            f"Hi {customer_name}, we could not complete your "
            f"subscription payment of ₹{amount:.2f}. "
            f"Please check your payment method."
        )

    return message