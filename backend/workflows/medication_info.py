from workflows.utils.fetch_medication import get_medication_by_name

def handle(message: str):
    med = get_medication_by_name(message)
    if not med:
        return {
            "type": "medication_info",
            "context": "Medication not found."
        }

    return {
        "type": "medication_info",
        "context": f"""
Medication name: {med['name']}
Generic name: {med['generic_name']}
Form: {med['form']}
Strength: {med['strength']}
Warnings: {med['warnings_en']}
"""
    }
