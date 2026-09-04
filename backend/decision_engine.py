# ============================================================
# REVIVE AI - RECOVERY DECISION ENGINE
# ============================================================


def choose_action(
    failure_type,
    recovery_probability,
    retry_count,
    successful_payments,
    failed_payments
):
    """
    Decide what recovery action should be taken
    for a failed subscription payment.
    """

    # --------------------------------------------------------
    # RULE 1: TOO MANY RETRIES
    # --------------------------------------------------------

    if retry_count >= 3:
        return {
            "action": "STOP",
            "reason": "Maximum retry limit reached."
        }


    # --------------------------------------------------------
    # RULE 2: EXPIRED CARD
    # --------------------------------------------------------

    if failure_type == "expired_card":

        return {
            "action": "UPDATE_PAYMENT_METHOD",
            "reason": (
                "The customer's card has expired. "
                "Retrying the same payment method is unlikely "
                "to solve the problem."
            )
        }


    # --------------------------------------------------------
    # RULE 3: INVALID CARD
    # --------------------------------------------------------

    if failure_type == "invalid_card":

        return {
            "action": "UPDATE_PAYMENT_METHOD",
            "reason": (
                "The payment method appears invalid. "
                "The customer should update their payment method."
            )
        }


    # --------------------------------------------------------
    # RULE 4: BANK TIMEOUT
    # --------------------------------------------------------

    if failure_type == "bank_timeout":

        if recovery_probability >= 0.70:

            return {
                "action": "RETRY_LATER",
                "reason": (
                    "Bank timeout appears temporary and the "
                    "predicted recovery probability is high."
                )
            }

        else:

            return {
                "action": "RETRY_LATER",
                "reason": (
                    "Bank timeout may be temporary, so a delayed "
                    "retry is safer than repeated immediate retries."
                )
            }


    # --------------------------------------------------------
    # RULE 5: INSUFFICIENT FUNDS
    # --------------------------------------------------------

    if failure_type == "insufficient_funds":

        if recovery_probability >= 0.75:

            return {
                "action": "SEND_REMINDER_AND_RETRY",
                "reason": (
                    "The customer has a high predicted recovery "
                    "probability. A reminder followed by a delayed "
                    "retry may recover the payment."
                )
            }

        elif recovery_probability >= 0.45:

            return {
                "action": "RETRY_LATER",
                "reason": (
                    "Recovery probability is moderate, so a delayed "
                    "retry is preferred."
                )
            }

        else:

            return {
                "action": "ESCALATE",
                "reason": (
                    "Recovery probability is low. Further automated "
                    "attempts may waste retries."
                )
            }


    # --------------------------------------------------------
    # RULE 6: AUTHENTICATION FAILURE
    # --------------------------------------------------------

    if failure_type == "authentication_failed":

        if recovery_probability >= 0.60:

            return {
                "action": "RETRY_LATER",
                "reason": (
                    "Authentication failure may be temporary and "
                    "the customer has reasonable recovery potential."
                )
            }

        else:

            return {
                "action": "ESCALATE",
                "reason": (
                    "Authentication failure has a low predicted "
                    "recovery probability."
                )
            }


    # --------------------------------------------------------
    # DEFAULT
    # --------------------------------------------------------

    return {
        "action": "ESCALATE",
        "reason": (
            "Failure type is unknown or does not have a safe "
            "automated recovery strategy."
        )
    }