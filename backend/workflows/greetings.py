def handle(message: str):
    return {
        "type": "greeting",
        "context": (
            "Greet the user politely and briefly. "
            "Explain that you can provide factual information about medications, "
            "check availability, and help with prescription status."
        )
    }
