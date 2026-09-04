# ============================================================
# REVIVE AI - RAZORPAY WEBHOOK
# ============================================================

import os
import json
import hmac
import hashlib

from fastapi import APIRouter, Request, HTTPException

from backend.database import (
    insert_payment,
    update_payment_result,
    insert_recovery_action
)

from backend.recovery_agent import recovery_agent
from backend.action_executor import execute_action


router = APIRouter()


# ============================================================
# WEBHOOK SECRET
# ============================================================

WEBHOOK_SECRET = os.getenv(
    "RAZORPAY_WEBHOOK_SECRET",
    ""
)


# ============================================================
# VERIFY RAZORPAY SIGNATURE
# ============================================================

def verify_signature(
    raw_body: bytes,
    received_signature: str
):

    if not WEBHOOK_SECRET:

        raise HTTPException(
            status_code=500,
            detail="Razorpay webhook secret is not configured."
        )

    expected_signature = hmac.new(
        WEBHOOK_SECRET.encode("utf-8"),
        raw_body,
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(
        expected_signature,
        received_signature
    )


# ============================================================
# WEBHOOK ENDPOINT
# ============================================================

@router.post("/webhook/razorpay")
async def razorpay_webhook(
    request: Request
):

    # --------------------------------------------------------
    # READ RAW BODY
    # --------------------------------------------------------

    raw_body = await request.body()

    received_signature = request.headers.get(
        "X-Razorpay-Signature"
    )

    if not received_signature:

        raise HTTPException(
            status_code=400,
            detail="Missing X-Razorpay-Signature header."
        )


    # --------------------------------------------------------
    # VERIFY SIGNATURE
    # --------------------------------------------------------

    if not verify_signature(
        raw_body,
        received_signature
    ):

        raise HTTPException(
            status_code=400,
            detail="Invalid Razorpay webhook signature."
        )


    # --------------------------------------------------------
    # PARSE JSON AFTER SIGNATURE VERIFICATION
    # --------------------------------------------------------

    try:

        payload = json.loads(
            raw_body.decode("utf-8")
        )

    except json.JSONDecodeError:

        raise HTTPException(
            status_code=400,
            detail="Invalid JSON payload."
        )


    event = payload.get("event")


    print()
    print("=" * 70)
    print("Razorpay webhook received")
    print("Event:", event)
    print("=" * 70)


    # ========================================================
    # HANDLE PAYMENT FAILED
    # ========================================================

    if event == "payment.failed":

        payment = (
            payload
            .get("payload", {})
            .get("payment", {})
            .get("entity", {})
        )


        # ----------------------------------------------------
        # EXTRACT PAYMENT INFORMATION
        # ----------------------------------------------------

        payment_id = payment.get(
            "id"
        )

        amount = payment.get(
            "amount",
            0
        )

        amount_rupees = amount / 100


        payment_method = payment.get(
            "method",
            "unknown"
        )


        # ----------------------------------------------------
        # EXTRACT FAILURE INFORMATION
        # ----------------------------------------------------

        failure_type = payment.get(
            "error_reason",
            "payment_failed"
        )

        error_code = payment.get(
            "error_code",
            ""
        )

        error_description = payment.get(
            "error_description",
            ""
        )

        error_source = payment.get(
            "error_source",
            ""
        )

        error_step = payment.get(
            "error_step",
            ""
        )


        # ----------------------------------------------------
        # EXTRACT CUSTOMER INFORMATION
        # ----------------------------------------------------

        customer_email = payment.get(
            "email",
            ""
        )

        customer_contact = payment.get(
            "contact",
            ""
        )


        # ----------------------------------------------------
        # CREATE INTERNAL PAYMENT OBJECT
        # ----------------------------------------------------

        payment_data = {

            "payment_id":
                payment_id or
                "unknown_payment",

            "subscription_id":
                "",

            "customer_id":
                "",

            "customer_name":
                "Razorpay Customer",

            "payment_amount":
                amount_rupees,

            "failure_type":
                failure_type,

            "retry_count":
                0,

            "successful_payments":
                0,

            "failed_payments":
                1,

            "customer_age_days":
                0,

            "days_since_failure":
                0,

            "payment_method":
                payment_method,

            "previous_recovery_rate":
                0
        }


        # ----------------------------------------------------
        # PRINT FAILURE DETAILS
        # ----------------------------------------------------

        print("Payment ID:", payment_id)
        print("Amount: ₹", amount_rupees)
        print("Payment Method:", payment_method)
        print("Failure Type:", failure_type)
        print("Error Code:", error_code)
        print("Error Source:", error_source)
        print("Error Step:", error_step)
        print("Error Description:", error_description)
        print("Customer Email:", customer_email)
        print("Customer Contact:", customer_contact)


        # ----------------------------------------------------
        # SAVE FAILED PAYMENT
        # ----------------------------------------------------

        insert_payment(
            payment_data
        )


        # ----------------------------------------------------
        # RUN REVIVE AI
        # ----------------------------------------------------

        decision = recovery_agent(
            payment_data
        )


        print()
        print("REVIVE AI DECISION")
        print("-------------------")
        print(
            "Recovery Probability:",
            decision["recovery_probability"]
        )
        print(
            "Recommended Action:",
            decision["recommended_action"]
        )
        print(
            "Final Action:",
            decision["final_action"]
        )
        print(
            "Guardrail:",
            (
                "PASSED"
                if decision["guardrail_allowed"]
                else "BLOCKED"
            )
        )


        # ----------------------------------------------------
        # EXECUTE ACTION
        # ----------------------------------------------------

        result = execute_action(

            payment_data,

            decision["final_action"],

            decision["recovery_probability"]
        )


        # ----------------------------------------------------
        # DETERMINE RESULT
        # ----------------------------------------------------

        recovered = (
            result["status"] == "SUCCESS"
        )

        recovered_amount = result.get(
            "recovered_amount",
            0
        )


        # ----------------------------------------------------
        # SAVE PAYMENT RESULT
        # ----------------------------------------------------

        update_payment_result(

            payment_id=
                payment_data["payment_id"],

            recovery_probability=
                decision["recovery_probability"],

            recommended_action=
                decision["recommended_action"],

            final_action=
                decision["final_action"],

            guardrail_allowed=
                decision["guardrail_allowed"],

            status=
                result["status"],

            recovered=
                recovered,

            recovered_amount=
                recovered_amount
        )


        # ----------------------------------------------------
        # SAVE ACTION HISTORY
        # ----------------------------------------------------

        insert_recovery_action(

            payment_id=
                payment_data["payment_id"],

            action=
                decision["final_action"],

            reason=
                decision["reason"],

            recovery_probability=
                decision["recovery_probability"],

            guardrail_allowed=
                decision["guardrail_allowed"],

            result=
                result["status"],

            recovered_amount=
                recovered_amount
        )


        # ----------------------------------------------------
        # RETURN RESULT
        # ----------------------------------------------------

        return {

            "status":
                "processed",

            "event":
                event,

            "payment_id":
                payment_data["payment_id"],

            "recovery_probability":
                decision["recovery_probability"],

            "recommended_action":
                decision["recommended_action"],

            "final_action":
                decision["final_action"],

            "guardrail":
                (
                    "PASSED"
                    if decision["guardrail_allowed"]
                    else "BLOCKED"
                ),

            "result":
                result["status"],

            "recovered_amount":
                recovered_amount
        }


    # ========================================================
    # IGNORE OTHER EVENTS
    # ========================================================

    return {

        "status":
            "ignored",

        "event":
            event
    }