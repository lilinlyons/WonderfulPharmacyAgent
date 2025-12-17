# workflows/active_ingredients.py
from utils.logging_utils.workflow_logger import get_workflow_logger
from workflows.utils.fetch_medication import get_medication_by_name

def handle(message: str, user_id: str | None = None):
    """
    Workflow: Active ingredients lookup
    """
    logger = get_workflow_logger(user_id)
    logger.info("Workflow started")
    logger.info("Input message: %s", message)

    try:
        med = get_medication_by_name(message)
    except Exception:
        logger.exception("Failed to fetch medication")
        return {
            "type": "active_ingredients",
            "context": "Sorry, there was an internal error while retrieving the medication information."
        }

    if not med:
        logger.info("Medication not found")
        return {
            "type": "active_ingredients",
            "context": "Medication not found in the system."
        }

    logger.info(
        "Medication found: name=%s active_ingredient=%s",
        med.get("name"),
        med.get("active_ingredient"),
    )

    return {
        "type": "active_ingredients",
        "context": (
            f"Medication name: {med['name']}\n"
            f"Active ingredient(s): {med['active_ingredient']}"
        )
    }
