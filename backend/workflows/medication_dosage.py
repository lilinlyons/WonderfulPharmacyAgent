from workflows.utils.fetch_medication import get_medication_by_name

def handle(message: str):
    med = get_medication_by_name(message)
    if not med:
        return {
            "type": "medication_dosage",
            "context": "Medication not found."
        }

    return {
        "type": "medication_dosage",
        "context": f"""
Medication name: {med['name']}
Label dosage instructions:
{med['label_instructions_en']}

For personalized dosing or medical advice, please consult a pharmacist or doctor.
"""
    }
