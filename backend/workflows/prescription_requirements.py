from workflows.utils.fetch_medication import get_medication_by_name

def handle(message: str):
    med = get_medication_by_name(message)

    if not med:
        return {
            "type": "prescription_requirement",
            "context": "Medication not found."
        }

    return {
        "type": "prescription_requirement",
        "context": f"""
Medication name: {med['name']}
Prescription required: {"Yes" if med['rx_required'] else "No"}
"""
    }