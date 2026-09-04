# ============================================================
# REVIVE AI - GUARDRAIL ENGINE
# ============================================================

MAX_RETRIES = 3
MAX_MESSAGES = 2


def check_action(payment, action):
    """
    Checks whether an action is safe to execute.

    AI recommends an action.
    Guardrails decide whether that action is allowed.
    """

    # --------------------------------------------------------
    # RULE 1 - CANCELLED SUBSCRIPTION
    # --------------------------------------------------------

    if payment.get("cancelled", False):

        return {
            "allowed": False,
            "action": "STOP",
            "reason": "Subscription has been cancelled."
        }


    # --------------------------------------------------------
    # RULE 2 - CUSTOMER OPTED OUT
    # --------------------------------------------------------

    if payment.get("opted_out", False):

        return {
            "allowed": False,
            "action": "STOP",
            "reason": "Customer has opted out of recovery messages."
        }


    # --------------------------------------------------------
    # RULE 3 - MAXIMUM RETRIES
    # --------------------------------------------------------

    if payment.get("retry_count", 0) >= MAX_RETRIES:

        return {
            "allowed": False,
            "action": "STOP",
            "reason": "Maximum retry limit reached."
        }


    # --------------------------------------------------------
    # RULE 4 - MAXIMUM CUSTOMER MESSAGES
    # --------------------------------------------------------

    if (
        action in [
            "SEND_REMINDER_AND_RETRY",
            "SEND_REMINDER"
        ]
        and payment.get("message_count", 0) >= MAX_MESSAGES
    ):

        return {
            "allowed": False,
            "action": "STOP",
            "reason": "Maximum customer message limit reached."
        }


    # --------------------------------------------------------
    # ACTION APPROVED
    # --------------------------------------------------------

    return {
        "allowed": True,
        "action": action,
        "reason": "Action passed all guardrail checks."
    }