from dotenv import load_dotenv

load_dotenv()


from backend.webhook import router as webhook_router
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


from backend.database import (
    initialize_database,
    insert_payment,
    get_all_payments,
    get_payment,
    get_metrics,
    update_payment_result,
    insert_recovery_action
)

from backend.recovery_agent import recovery_agent

from backend.action_executor import execute_action


# ============================================================
# CREATE FASTAPI APP
# ============================================================

app = FastAPI(
    title="Revive AI",
    description="AI Subscription Revenue Recovery API",
    version="1.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    webhook_router
)
# ============================================================
# INITIALIZE DATABASE
# ============================================================

initialize_database()


# ============================================================
# PAYMENT REQUEST MODEL
# ============================================================

class PaymentFailure(BaseModel):

    payment_id: str

    subscription_id: str = ""

    customer_id: str = ""

    customer_name: str = "Customer"

    payment_amount: float

    failure_type: str

    retry_count: int = 0

    successful_payments: int = 0

    failed_payments: int = 0

    customer_age_days: int = 0

    days_since_failure: float = 0

    payment_method: str = "card"

    previous_recovery_rate: float = 0

    simulated_retry_success: bool = False

# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():

    return {
        "application": "Revive AI",
        "status": "running"
    }


# ============================================================
# CREATE FAILED PAYMENT
# ============================================================

@app.post("/payments/failure")
def create_payment_failure(
    payment: PaymentFailure
):

    payment_data = payment.model_dump()

    # Store payment
    insert_payment(
        payment_data
    )


    # Run recovery AI
    decision = recovery_agent(
        payment_data
    )


    # Execute approved action
    result = execute_action(

        payment_data,

        decision["final_action"],

        decision["recovery_probability"]

    )


    # Determine recovery status
    recovered = (
        result["status"] == "SUCCESS"
    )


    recovered_amount = result.get(
        "recovered_amount",
        0
    )


    # Save result
    update_payment_result(

        payment_id=payment.payment_id,

        recovery_probability=
            decision["recovery_probability"],

        recommended_action=
            decision["recommended_action"],

        final_action=
            decision["final_action"],

        guardrail_allowed=
            decision["guardrail_allowed"],

        status=result["status"],

        recovered=recovered,

        recovered_amount=recovered_amount
    )


    # Save action history
    insert_recovery_action(

        payment_id=payment.payment_id,

        action=decision["final_action"],

        reason=decision["reason"],

        recovery_probability=
            decision["recovery_probability"],

        guardrail_allowed=
            decision["guardrail_allowed"],

        result=result["status"],

        recovered_amount=recovered_amount
    )


    return {

        "payment_id":
            payment.payment_id,

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


# ============================================================
# GET ALL PAYMENTS
# ============================================================

@app.get("/payments")
def payments():

    return get_all_payments()


# ============================================================
# GET ONE PAYMENT
# ============================================================

@app.get("/payments/{payment_id}")
def payment_details(
    payment_id: str
):

    payment = get_payment(
        payment_id
    )

    if payment is None:

        raise HTTPException(
            status_code=404,
            detail="Payment not found"
        )

    return payment


# ============================================================
# GET METRICS
# ============================================================

@app.get("/metrics")
def metrics():

    return get_metrics()