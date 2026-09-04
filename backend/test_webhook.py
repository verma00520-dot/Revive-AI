import json
import hmac
import hashlib
import requests


# Same secret as your .env
WEBHOOK_SECRET = "revive_test_secret_2026"


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
                "error_description": "Payment failed because the bank declined the transaction.",
                "error_source": "bank",
                "error_step": "payment_authorization",
                "error_reason": "card_declined"
            }
        }
    }
}


# Convert to JSON
raw_body = json.dumps(
    payload,
    separators=(",", ":")
).encode("utf-8")


# Generate Razorpay-style signature
signature = hmac.new(
    WEBHOOK_SECRET.encode("utf-8"),
    raw_body,
    hashlib.sha256
).hexdigest()


# Send webhook
response = requests.post(
    "http://127.0.0.1:8000/webhook/razorpay",

    data=raw_body,

    headers={
        "Content-Type": "application/json",
        "X-Razorpay-Signature": signature
    }
)


print()
print("=" * 60)
print("WEBHOOK TEST RESULT")
print("=" * 60)

print("HTTP Status:", response.status_code)

print()
print("Response:")
print(response.text)