import uuid
from datetime import datetime
from workflows.db.db import conn
from utils.workflow_logger import get_workflow_logger

logger = get_workflow_logger()

def handle(message: str, user_id: str | None = None):
    logger.info("Support request workflow started")

    if not user_id:
        logger.warning("Missing user_id for support request")
        return {
            "type": "support_request",
            "context": "Unable to open a support request. User not identified."
        }

    request_id = str(uuid.uuid4())
    created_at = datetime.utcnow().isoformat()
    status = "open"

    try:
        c = conn()
        cur = c.cursor()

        cur.execute(
            """
            INSERT INTO support_requests
            (id, user_id, subject, message, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                request_id,
                user_id,
                "General Support",
                message,
                status,
                created_at,
            )
        )

        c.commit()
        c.close()

        logger.info("Support request created: %s", request_id)

        return {
            "type": "support_request",
            "context": (
                "**Support request opened successfully**\n\n"
                f"• **Request ID:** {request_id}\n"
                f"• **Status:** {status.capitalize()}\n"
                f"• **Submitted at:** {created_at}\n\n"
                "A pharmacist or support agent will contact you shortly."
            ),
            "data": {
                "id": request_id,
                "user_id": user_id,
                "status": status,
                "subject": "General Support",
                "message": message,
                "created_at": created_at,
            }
        }

    except Exception:
        logger.exception("Failed to create support request")
        return {
            "type": "support_request",
            "context": (
                "Sorry, we couldn't open your support request.\n"
                "Please try again later."
            )
        }
