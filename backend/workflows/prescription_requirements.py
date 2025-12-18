# workflows/prescription_requirement.py
from utils.fetch_medication import get_medication_by_name
from utils.logging_utils.workflow_logger import get_workflow_logger


def handle(message: str, user_id: str | None = None):
    logger = get_workflow_logger(user_id)
    logger.info("Workflow started")
    logger.info("Input message: %s", message)

    try:
        med = get_medication_by_name(message)
    except Exception:
        logger.exception("Failed to fetch medication")
        return {
            "type": "prescription_requirement",
            "context": (
                "Sorry, there was an internal error while retrieving the medication information."
            )
        }

    if not med:
        logger.info("Medication not found")
        return {
            "type": "prescription_requirement",
            "context": "Medication not found."
        }

    logger.info(
        "Medication found: name=%s rx_required=%s",
        med.get("name"),
        med.get("rx_required"),
    )

    return {
        "type": "prescription_requirement",
        "context": (
            f"Medication name: {med['name']}\n"
            f"Prescription required: {'Yes, please contact your Doctor if you require a prescription.' if med['rx_required'] else 'No'}"
        )
    }
