# workflows/active_ingredients.py
from workflows.utils.fetch_medication import get_medication_by_name

def handle(message: str):
    """
    Workflow: Active ingredients lookup
    """
    med = get_medication_by_name(message)

    if not med:
        return {
            "type": "active_ingredients",
            "context": "Medication not found in the system."
        }

    return {
        "type": "active_ingredients",
        "context": f"""
Medication name: {med['name']}
Active ingredient(s): {med['active_ingredient']}
"""
    }
