def handle(message: str, user_id: str | None = None):
    return {
        "type": "fallback",
        "context": (
            "I’m not sure I fully understood your request. "
            "I can help with:\n"
            "- Medication information\n"
            "- Active ingredients\n"
            "- Prescription requirements\n"
            "- Stock availability\n"
            "- Prescription refill status\n\n"
            "Could you please rephrase or clarify your question?"
        )
    }
