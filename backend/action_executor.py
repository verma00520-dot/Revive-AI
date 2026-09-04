# ============================================================
# REVIVE AI - ACTION EXECUTOR
# ============================================================


from backend.simulator import simulate_retry, simulate_message


def execute_action(payment, action, recovery_probability):

    # --------------------------------------------------------
    # RETRY NOW
    # --------------------------------------------------------

    if action == "RETRY_NOW":

        print("\nExecuting immediate retry...")

        result = simulate_retry(
            payment,
            recovery_probability
        )

        return {
            "action": action,
            "status": result["status"],
            "recovered_amount": result["recovered_amount"]
        }


    # --------------------------------------------------------
    # RETRY LATER
    # --------------------------------------------------------

    elif action == "RETRY_LATER":

        print("\nScheduling delayed retry...")

        # For the prototype we simulate the retry immediately.
        # In a production system this would use a scheduler.

        result = simulate_retry(
            payment,
            recovery_probability
        )

        return {
            "action": action,
            "status": result["status"],
            "recovered_amount": result["recovered_amount"]
        }


    # --------------------------------------------------------
    # SEND REMINDER + RETRY
    # --------------------------------------------------------

    elif action == "SEND_REMINDER_AND_RETRY":

        print("\nSending customer reminder...")

        message = simulate_message(
            payment
        )

        print("\nMESSAGE:")
        print(message)

        payment["message_count"] = (
            payment.get("message_count", 0) + 1
        )

        print("\nRetrying payment...")

        result = simulate_retry(
            payment,
            recovery_probability
        )

        return {
            "action": action,
            "status": result["status"],
            "recovered_amount": result["recovered_amount"],
            "message": message
        }


    # --------------------------------------------------------
    # UPDATE PAYMENT METHOD
    # --------------------------------------------------------

    elif action == "UPDATE_PAYMENT_METHOD":

        print("\nPayment method update required.")

        message = simulate_message(
            payment
        )

        print("\nMESSAGE:")
        print(message)

        return {
            "action": action,
            "status": "WAITING_FOR_CUSTOMER",
            "recovered_amount": 0,
            "message": message
        }


    # --------------------------------------------------------
    # ESCALATE
    # --------------------------------------------------------

    elif action == "ESCALATE":

        print("\nEscalating payment for human review.")

        return {
            "action": action,
            "status": "ESCALATED",
            "recovered_amount": 0
        }


    # --------------------------------------------------------
    # STOP
    # --------------------------------------------------------

    elif action == "STOP":

        print("\nRecovery process stopped.")

        return {
            "action": action,
            "status": "STOPPED",
            "recovered_amount": 0
        }


    # --------------------------------------------------------
    # UNKNOWN ACTION
    # --------------------------------------------------------

    else:

        return {
            "action": action,
            "status": "UNKNOWN_ACTION",
            "recovered_amount": 0
        }