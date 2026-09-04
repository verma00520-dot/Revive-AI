from recovery_agent import recovery_agent
from action_executor import execute_action
from audit_log import create_log, print_log


# ============================================================
# DEMO PAYMENT
# ============================================================

payment = {

    "payment_id": "pay_demo_001",

    "customer_name": "Rahul",

    "payment_amount": 999,

    "failure_type": "insufficient_funds",

    "retry_count": 0,

    "successful_payments": 11,

    "failed_payments": 1,

    "customer_age_days": 320,

    "days_since_failure": 0.5,

    "payment_method": "card",

    "previous_recovery_rate": 0.917,

    "message_count": 0,

    "cancelled": False,

    "opted_out": False,

    "simulated_retry_success": True
}


# ============================================================
# AUDIT HISTORY
# ============================================================

history = []


def log_event(event, details=None):

    log = create_log(
        payment["payment_id"],
        event,
        details
    )

    history.append(log)

    print_log(log)


# ============================================================
# START RECOVERY
# ============================================================

print()
print("=" * 70)
print("              REVIVE AI - RECOVERY AGENT")
print("=" * 70)


log_event(
    "PAYMENT_FAILED",
    {
        "amount": payment["payment_amount"],
        "failure_type": payment["failure_type"]
    }
)


# ============================================================
# RUN AI
# ============================================================

decision = recovery_agent(
    payment
)


log_event(
    "AI_ANALYSIS_COMPLETED",
    {
        "recovery_probability":
            decision["recovery_probability"]
    }
)


# ============================================================
# SHOW DECISION
# ============================================================

print()

print(
    "Recovery Probability:",
    f"{decision['recovery_probability'] * 100:.2f}%"
)

print()

print(
    "AI Recommended Action:",
    decision["recommended_action"]
)

print()

print(
    "Guardrail:",
    "PASSED"
    if decision["guardrail_allowed"]
    else "BLOCKED"
)

print()

print(
    "Final Action:",
    decision["final_action"]
)

print()

print(
    "Reason:",
    decision["reason"]
)


log_event(
    "RECOVERY_DECISION",
    {
        "recommended_action":
            decision["recommended_action"],

        "final_action":
            decision["final_action"],

        "guardrail_allowed":
            decision["guardrail_allowed"]
    }
)


# ============================================================
# STOP IF BLOCKED
# ============================================================

if decision["final_action"] == "STOP":

    log_event(
        "RECOVERY_STOPPED",
        {
            "reason": decision["reason"]
        }
    )

else:

    # --------------------------------------------------------
    # EXECUTE ACTION
    # --------------------------------------------------------

    result = execute_action(
        payment,
        decision["final_action"],
        decision["recovery_probability"]
    )


    # --------------------------------------------------------
    # LOG RESULT
    # --------------------------------------------------------

    log_event(
        "ACTION_EXECUTED",
        {
            "action": result["action"],
            "status": result["status"]
        }
    )


    # --------------------------------------------------------
    # RECOVERY SUCCESS
    # --------------------------------------------------------

    if result["status"] == "SUCCESS":

        payment["recovered"] = True

        payment["recovered_amount"] = (
            result["recovered_amount"]
        )

        log_event(
            "PAYMENT_RECOVERED",
            {
                "amount":
                    result["recovered_amount"]
            }
        )


    # --------------------------------------------------------
    # RECOVERY FAILED
    # --------------------------------------------------------

    else:

        payment["recovered"] = False

        payment["recovered_amount"] = 0

        log_event(
            "PAYMENT_NOT_RECOVERED",
            {
                "status": result["status"]
            }
        )


# ============================================================
# FINAL RESULT
# ============================================================

print()
print("=" * 70)

if payment.get("recovered", False):

    print("✅ PAYMENT RECOVERED")

    print(
        f"Recovered Revenue: "
        f"₹{payment['recovered_amount']:.2f}"
    )

else:

    print("❌ PAYMENT NOT RECOVERED")

print("=" * 70)


# ============================================================
# AGENT TIMELINE
# ============================================================

print()
print("AGENT TIMELINE")
print("-" * 70)

for log in history:
    print_log(log)