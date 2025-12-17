# workflows/medication_info.py
from workflows.utils.fetch_medication import get_medication_by_name
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
            "type": "medication_info",
            "context": (
                "Sorry, there was an internal error while retrieving the medication information."
            )
        }

    if not med:
        logger.info("Medication not found")
        return {
            "type": "medication_info",
            "context": "Medication not found."
        }

    logger.info(
        "Medication found: name=%s generic_name=%s",
        med.get("name"),
        med.get("generic_name"),
    )

    return {
        "type": "medication_info",
        "context": (
            f"Medication name: {med['name']}\n"
            f"Generic name: {med['generic_name']}\n"
            f"Form: {med['form']}\n"
            f"Strength: {med['strength']}\n"
            f"Warnings: {med['warnings_en']}"
        )
    }
