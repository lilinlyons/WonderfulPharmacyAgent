from enum import Enum

class Intent(str, Enum):
    GREETING = "greeting"
    MEDICATION_INFO = "medication_info"
    ACTIVE_INGREDIENTS = "active_ingredients"
    PRESCRIPTION_REQUIREMENT = "prescription_requirement"
    MEDICATION_DOSAGE = "medication_dosage"
    STOCK_CHECK = "stock_check"
    REFILL_REQUEST = "refill_request"
    MEDICAL_ADVICE = "medical_advice"
    SIDE_EFFECTS_CONCERN = "side_effects_concern"
    DRUG_INTERACTIONS = "drug_interactions"
    SUPPORT = "support"
    UNKNOWN = "unknown"

# THIS ORDER IS CRITICAL — DO NOT CHANGE AFTER TRAINING
INTENT_LABELS = [
    Intent.GREETING,
    Intent.MEDICATION_INFO,
    Intent.ACTIVE_INGREDIENTS,
    Intent.PRESCRIPTION_REQUIREMENT,
    Intent.MEDICATION_DOSAGE,
    Intent.STOCK_CHECK,
    Intent.REFILL_REQUEST,
    Intent.MEDICAL_ADVICE,
    Intent.SIDE_EFFECTS_CONCERN,
    Intent.DRUG_INTERACTIONS,
    Intent.SUPPORT,
    Intent.UNKNOWN
]