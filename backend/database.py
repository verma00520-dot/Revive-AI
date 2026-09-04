import sqlite3


DATABASE_NAME = "revive.db"


# ============================================================
# GET DATABASE CONNECTION
# ============================================================

def get_connection():
    connection = sqlite3.connect(
        DATABASE_NAME
    )

    connection.row_factory = sqlite3.Row

    return connection


# ============================================================
# CREATE DATABASE TABLES
# ============================================================

def initialize_database():

    connection = get_connection()

    cursor = connection.cursor()


    # --------------------------------------------------------
    # PAYMENTS TABLE
    # --------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS payments (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            payment_id TEXT UNIQUE,

            subscription_id TEXT,

            customer_id TEXT,

            customer_name TEXT,

            amount REAL,

            failure_type TEXT,

            retry_count INTEGER DEFAULT 0,

            successful_payments INTEGER DEFAULT 0,

            failed_payments INTEGER DEFAULT 0,

            customer_age_days INTEGER DEFAULT 0,

            days_since_failure REAL DEFAULT 0,

            payment_method TEXT,

            previous_recovery_rate REAL DEFAULT 0,

            recovery_probability REAL,

            recommended_action TEXT,

            final_action TEXT,

            guardrail_allowed INTEGER,

            status TEXT,

            recovered INTEGER DEFAULT 0,

            recovered_amount REAL DEFAULT 0,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)


    # --------------------------------------------------------
    # RECOVERY ACTIONS TABLE
    # --------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recovery_actions (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            payment_id TEXT,

            action TEXT,

            reason TEXT,

            recovery_probability REAL,

            guardrail_allowed INTEGER,

            result TEXT,

            recovered_amount REAL DEFAULT 0,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)


    connection.commit()

    connection.close()


# ============================================================
# INSERT PAYMENT
# ============================================================

def insert_payment(payment):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO payments (

            payment_id,
            subscription_id,
            customer_id,
            customer_name,
            amount,
            failure_type,
            retry_count,
            successful_payments,
            failed_payments,
            customer_age_days,
            days_since_failure,
            payment_method,
            previous_recovery_rate,
            status
        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (

        payment.get("payment_id"),

        payment.get(
            "subscription_id",
            ""
        ),

        payment.get(
            "customer_id",
            ""
        ),

        payment.get(
            "customer_name",
            "Customer"
        ),

        payment.get(
            "payment_amount",
            0
        ),

        payment.get(
            "failure_type",
            "unknown"
        ),

        payment.get(
            "retry_count",
            0
        ),

        payment.get(
            "successful_payments",
            0
        ),

        payment.get(
            "failed_payments",
            0
        ),

        payment.get(
            "customer_age_days",
            0
        ),

        payment.get(
            "days_since_failure",
            0
        ),

        payment.get(
            "payment_method",
            ""
        ),

        payment.get(
            "previous_recovery_rate",
            0
        ),

        "FAILED"
    ))

    connection.commit()

    connection.close()


# ============================================================
# UPDATE PAYMENT AFTER RECOVERY
# ============================================================

def update_payment_result(
    payment_id,
    recovery_probability,
    recommended_action,
    final_action,
    guardrail_allowed,
    status,
    recovered,
    recovered_amount
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        UPDATE payments

        SET

            recovery_probability = ?,

            recommended_action = ?,

            final_action = ?,

            guardrail_allowed = ?,

            status = ?,

            recovered = ?,

            recovered_amount = ?,

            updated_at = CURRENT_TIMESTAMP

        WHERE payment_id = ?
    """, (

        recovery_probability,

        recommended_action,

        final_action,

        int(guardrail_allowed),

        status,

        int(recovered),

        recovered_amount,

        payment_id
    ))

    connection.commit()

    connection.close()


# ============================================================
# SAVE RECOVERY ACTION
# ============================================================

def insert_recovery_action(

    payment_id,
    action,
    reason,
    recovery_probability,
    guardrail_allowed,
    result,
    recovered_amount

):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO recovery_actions (

            payment_id,

            action,

            reason,

            recovery_probability,

            guardrail_allowed,

            result,

            recovered_amount

        )

        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (

        payment_id,

        action,

        reason,

        recovery_probability,

        int(guardrail_allowed),

        result,

        recovered_amount
    ))

    connection.commit()

    connection.close()


# ============================================================
# GET ALL PAYMENTS
# ============================================================

def get_all_payments():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM payments
        ORDER BY created_at DESC
    """)

    rows = cursor.fetchall()

    connection.close()

    return [dict(row) for row in rows]


# ============================================================
# GET ONE PAYMENT
# ============================================================

def get_payment(payment_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM payments
        WHERE payment_id = ?
    """, (payment_id,))

    row = cursor.fetchone()

    connection.close()

    if row:
        return dict(row)

    return None


# ============================================================
# GET RECOVERY METRICS
# ============================================================

def get_metrics():

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute("""
        SELECT
            COUNT(*) AS total_payments,
            COALESCE(SUM(amount), 0) AS revenue_at_risk,
            COALESCE(SUM(recovered_amount), 0) AS recovered_revenue,
            COALESCE(SUM(recovered), 0) AS recovered_count
        FROM payments
    """)

    row = cursor.fetchone()

    connection.close()

    total_payments = row["total_payments"]

    revenue_at_risk = row["revenue_at_risk"]

    recovered_revenue = row["recovered_revenue"]

    recovered_count = row["recovered_count"]


    if revenue_at_risk > 0:

        recovery_rate = (
            recovered_revenue /
            revenue_at_risk
        ) * 100

    else:

        recovery_rate = 0


    return {

        "total_payments": total_payments,

        "revenue_at_risk": round(
            revenue_at_risk,
            2
        ),

        "recovered_revenue": round(
            recovered_revenue,
            2
        ),

        "recovered_count": recovered_count,

        "recovery_rate": round(
            recovery_rate,
            2
        )
    }