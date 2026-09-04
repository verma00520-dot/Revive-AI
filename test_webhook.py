import json
import hmac
import hashlib
import requests


# ============================================================
# TEST WEBHOOK SECRET
# ============================================================

WEBHOOK_SECRET = "revive_test_secret_2026"


# ============================================================
# FAKE RAZORPAY PAYMENT.FAILED PAYLOAD
# ============================================================

payload = {
    "event": "payment.failed",

    "payload": {
        "payment": {
            "entity": {

                "id": "pay_webhook_test_001",

                "amount": 99900,

                "currency": "INR",

                "method": "card",

                "email": "test@example.com",

                "contact": "+919999999999",

                "error_code": "BAD_REQUEST_ERROR",

                "error_description":
                    "Payment failed because the bank declined the transaction.",

                "error_source": "bank",

                "error_step": "payment_authorization",

                "error_reason": "card_declined"
            }
        }
    }
}


# ============================================================
# CONVERT PAYLOAD TO RAW JSON
# ============================================================

raw_body = json.dumps(
    payload,
    separators=(",", ":")
).encode("utf-8")


# ============================================================
# GENERATE RAZORPAY-STYLE SIGNATURE
# ============================================================

signature = hmac.new(

    WEBHOOK_SECRET.encode("utf-8"),

    raw_body,

    hashlib.sha256

).hexdigest()


# ============================================================
# SEND WEBHOOK TO REVIVE AI
# ============================================================

response = requests.post(

    "http://127.0.0.1:8000/webhook/razorpay",

    data=raw_body,

    headers={

        "Content-Type":
            "application/json",

        "X-Razorpay-Signature":
            signature
    }
)


# ============================================================
# DISPLAY RESULT
# ============================================================

print()

print("=" * 60)

print("WEBHOOK TEST RESULT")

print("=" * 60)

print()

print(
    "HTTP Status:",
    response.status_code
)

print()

print("Response:")

print(
    response.text
)