from bert.labels import Intent
from workflows import (
active_ingredients,
greetings,
medication_dosage,
medication_info,
prescription_requirements,
stock_check,
safety_redirect,
)

def route(intent: Intent):
    if intent in {
        Intent.MEDICAL_ADVICE,
        Intent.SIDE_EFFECTS_CONCERN,
        Intent.DRUG_INTERACTIONS,
    }:
        return safety_redirect.handle

    if intent == Intent.STOCK_CHECK:
        return stock_check.handle

    if intent == Intent.ACTIVE_INGREDIENTS:
        return active_ingredients.handle

    if intent == Intent.PRESCRIPTION_REQUIREMENT:
        return prescription_requirements.handle

    if intent == Intent.UNKNOWN:
        return safety_redirect.handle

    if intent == Intent.GREETING:
        return greetings.handle

    if intent == Intent.MEDICATION_INFO:
        return medication_info.handle

    if intent == Intent.MEDICATION_DOSAGE:
        return medication_dosage.handle

    # Intent.SUPPORT,
    # refill request
    # medication dosage


    return safety_redirect.handle
