# ============================================================
# REVIVE AI - AUDIT LOG
# ============================================================

from datetime import datetime


def create_log(
    payment_id,
    event,
    details=None
):

    return {
        "timestamp": datetime.now().isoformat(
            timespec="seconds"
        ),
        "payment_id": payment_id,
        "event": event,
        "details": details or {}
    }


def print_log(log):

    print(
        f"[{log['timestamp']}] "
        f"{log['payment_id']} - "
        f"{log['event']}"
    )

    if log["details"]:
        print(
            "   Details:",
            log["details"]
        )