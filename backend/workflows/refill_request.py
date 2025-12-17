import uuid
from datetime import datetime
from workflows.db.db import conn
from utils.workflow_logger import get_workflow_logger

logger = get_workflow_logger()

def handle(message: str, user_id: str | None = None):
    logger.info("Refill request workflow started")

    if not user_id:
        logger.warning("Missing user_id for refill request")
        return {
            "type": "refill_request",
            "context": "Unable to submit refill request. User not identified."
        }

    request_id = str(uuid.uuid4())
    created_at = datetime.utcnow().isoformat()
    status = "pending"

    try:
        c = conn()
        cur = c.cursor()

        cur.execute(
            """
            SELECT id, medication_id, refills_left, expires_on
            FROM prescriptions
            WHERE user_id = ?
              AND status = 'active'
            LIMIT 1
            """,
            (user_id,)
        )

        prescription = cur.fetchone()

        if not prescription:
            c.close()
            return {
                "type": "refill_request",
                "context": (
                    "**Refill request denied**\n\n"
                    "You do not have an active prescription on file.\n"
                    "Please contact your pharmacist or doctor."
                )
            }

        prescription_id, medication_id, refills_left, expires_on = prescription

        if refills_left is None or refills_left <= 0:
            c.close()
            return {
                "type": "refill_request",
                "context": (
                    "**No refills remaining**\n\n"
                    "Your prescription has no refills left.\n"
                    "Please contact your doctor."
                )
            }

        cur.execute(
            """
            INSERT INTO prescription_requests
            (id, user_id, medication_id, request_type, status, notes, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                request_id,
                user_id,
                medication_id,
                "refill",
                status,
                message,
                created_at,
            )
        )

        # ➖ 3. Deduct one refill
        cur.execute(
            """
            UPDATE prescriptions
            SET refills_left = refills_left - 1
            WHERE id = ?
            """,
            (prescription_id,)
        )

        c.commit()
        c.close()

        logger.info("Refill request created and refill deducted: %s", request_id)

        return {
            "type": "refill_request",
            "context": (
                "**Refill request submitted successfully**\n\n"
                f"• **Request ID:** {request_id}\n"
                f"• **Status:** {status.capitalize()}\n"
                f"• **Medication ID:** {medication_id}\n"
                f"• **Remaining refills:** {refills_left - 1}\n"
                f"• **Notes:** {message}\n"
                f"• **Submitted at:** {created_at}\n\n"
                "A pharmacist will review your request shortly. Please view the 'Prescription Requests' section for updates."
            ),
            "data": {
                "request_id": request_id,
                "user_id": user_id,
                "medication_id": medication_id,
                "status": status,
                "refills_left": refills_left - 1,
                "created_at": created_at,
            }
        }

    except Exception:
        logger.exception("Failed to create refill request")
        try:
            c.rollback()
            c.close()
        except Exception:
            pass

        return {
            "type": "refill_request",
            "context": "Sorry, we couldn't submit your refill request. Please try again."
        }
