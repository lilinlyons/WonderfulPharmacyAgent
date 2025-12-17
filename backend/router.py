import logging
from bert.labels import Intent
from workflows import (
    active_ingredients,
    fallback,
    greetings,
    medication_dosage,
    medication_info,
    prescription_requirements,
    stock_check,
    safety_redirect,
)

logger = logging.getLogger("pharmacy-agent")


def route(intent: Intent):
    """
    Route an intent to the correct workflow handler.
    Always returns a callable handler.
    """

    try:
        logger.info("Routing intent: %s", intent)

        if intent in {
            Intent.MEDICAL_ADVICE,
            Intent.SIDE_EFFECTS_CONCERN,
            Intent.DRUG_INTERACTIONS,
        }:
            logger.debug("Intent mapped to safety_redirect")
            return safety_redirect.handle

        if intent == Intent.STOCK_CHECK:
            logger.debug("Intent mapped to stock_check")
            return stock_check.handle

        if intent == Intent.ACTIVE_INGREDIENTS:
            logger.debug("Intent mapped to active_ingredients")
            return active_ingredients.handle

        if intent == Intent.PRESCRIPTION_REQUIREMENT:
            logger.debug("Intent mapped to prescription_requirements")
            return prescription_requirements.handle

        if intent == Intent.GREETING:
            logger.debug("Intent mapped to greetings")
            return greetings.handle

        if intent == Intent.MEDICATION_INFO:
            logger.debug("Intent mapped to medication_info")
            return medication_info.handle

        if intent == Intent.MEDICATION_DOSAGE:
            logger.debug("Intent mapped to medication_dosage")
            return medication_dosage.handle

        # Intent.SUPPORT
        # Intent.REFILL_REQUEST
        # → not implemented yet

        logger.info("No explicit route for intent %s, using fallback", intent)
        return fallback.handle

    except Exception:
        logger.exception("Routing failed for intent: %s", intent)
        return fallback.handle
