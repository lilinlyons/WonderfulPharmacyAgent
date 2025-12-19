from utils.medication.fetch_medication import get_medication_by_name
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
            "type": "medication_dosage",
            "context": (
                "Sorry, there was an internal error while retrieving the medication information."
            )
        }

    if not med:
        logger.info("Medication not found")
        return {
            "type": "medication_dosage",
            "context": "Medication not found."
        }

    logger.info(
        "Medication found: name=%s",
        med.get("name"),
    )

    return {
        "type": "medication_dosage",
        "context": (
            f"Medication name: {med['name']}\n"
            f"Label dosage instructions:\n"
            f"{med['label_instructions_en']}\n\n"
            "For personalized dosing or medical advice, please consult a pharmacist or doctor."
        )
    }