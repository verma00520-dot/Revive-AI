import pandas as pd
import joblib

from backend.decision_engine import choose_action
from backend.guardrails import check_action

# ============================================================
# LOAD TRAINED ML MODEL
# ============================================================

MODEL_PATH = "models/recovery_model.pkl"
model = joblib.load(MODEL_PATH)

# Compatibility fix for the saved LogisticRegression model
try:
    if hasattr(model, "steps"):
        model.steps[-1][1].multi_class = "auto"
    elif hasattr(model, "multi_class") is False:
        model.multi_class = "auto"
except Exception:
    pass


# ============================================================
# RECOVERY AGENT
# ============================================================

def recovery_agent(payment):
    """
    Complete recovery decision process.

    Input:
        payment = dictionary containing payment information

    Output:
        recovery decision dictionary
    """

    # --------------------------------------------------------
    # Convert payment dictionary into DataFrame
    # --------------------------------------------------------

    payment_df = pd.DataFrame([{
        "payment_amount": payment["payment_amount"],
        "failure_type": payment["failure_type"],
        "retry_count": payment["retry_count"],
        "successful_payments": payment["successful_payments"],
        "failed_payments": payment["failed_payments"],
        "customer_age_days": payment["customer_age_days"],
        "days_since_failure": payment["days_since_failure"],
        "payment_method": payment["payment_method"],
        "previous_recovery_rate": payment["previous_recovery_rate"]
    }])


    # --------------------------------------------------------
    # STEP 1 — PREDICT RECOVERY PROBABILITY
    # --------------------------------------------------------

    recovery_probability = model.predict_proba(
        payment_df
    )[0][1]


    # --------------------------------------------------------
    # STEP 2 — DECIDE WHAT TO DO
    # --------------------------------------------------------

    decision = choose_action(
        failure_type=payment["failure_type"],
        recovery_probability=recovery_probability,
        retry_count=payment["retry_count"],
        successful_payments=payment["successful_payments"],
        failed_payments=payment["failed_payments"]
    )


    # --------------------------------------------------------
    # STEP 3 — RETURN COMPLETE AGENT DECISION
    # --------------------------------------------------------

        # --------------------------------------------------------
    # STEP 3 — APPLY GUARDRAILS
    # --------------------------------------------------------

    guardrail_result = check_action(
        payment,
        decision["action"]
    )


    # --------------------------------------------------------
    # FINAL ACTION
    # --------------------------------------------------------

    if guardrail_result["allowed"]:

        final_action = decision["action"]

        final_reason = decision["reason"]

    else:

        final_action = guardrail_result["action"]

        final_reason = guardrail_result["reason"]


    # --------------------------------------------------------
    # RETURN COMPLETE DECISION
    # --------------------------------------------------------

    return {
        "payment_id": payment.get(
            "payment_id",
            "unknown"
        ),

        "recovery_probability": round(
            recovery_probability,
            4
        ),

        "recommended_action": decision["action"],

        "final_action": final_action,

        "decision_reason": decision["reason"],

        "guardrail_allowed": guardrail_result["allowed"],

        "guardrail_reason": guardrail_result["reason"],

        "reason": final_reason
    }
# ============================================================
# TEST THE AGENT
# ============================================================

if __name__ == "__main__":

    test_payment = {

        "payment_id": "pay_test_001",

        "payment_amount": 999,

        "failure_type": "bank_timeout",

        "retry_count": 0,

        "successful_payments": 11,

        "failed_payments": 1,

        "customer_age_days": 320,

        "days_since_failure": 0.5,

        "payment_method": "card",

        "previous_recovery_rate": 0.917
    }


    # Run agent
    result = recovery_agent(
        test_payment
    )


    # --------------------------------------------------------
    # DISPLAY RESULT
    # --------------------------------------------------------

    print()
    print("=" * 60)
    print("            REVIVE AI - RECOVERY AGENT")
    print("=" * 60)

    print()
    print("Payment ID:")
    print(result["payment_id"])

    print()
    print("Recovery Probability:")
    print(
        f"{result['recovery_probability'] * 100:.2f}%"
    )

    print()
    print("AI Recommended Action:")
    print(result["recommended_action"])

    print()
    print("Guardrail:")
    print(
        "PASSED"
        if result["guardrail_allowed"]
        else "BLOCKED"
    )

    print()
    print("Final Action:")
    print(result["final_action"])

    print()
    print("Reason:")
    print(result["reason"])

    print()
    print("=" * 60)