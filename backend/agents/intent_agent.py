from bert.labels import Intent
from bert.classifier import classify_intent


class IntentAgent:
    """
    Handles intent classification and routing to the correct workflow.
    """

    def __init__(self, logger):
        """
        :param logger: injected logger instance
        """
        self.classify_intent = classify_intent
        self.logger = logger

    def process(self, user_message: str, user_id: str):
        """
        Returns (system_context, user_prompt)
        """
        # ---- Intent classification ----
        try:
            intent = self.classify_intent(user_message)
            self.logger.info("Intent: %s", intent)
        except Exception:
            self.logger.exception("Intent classification failed")
            intent = Intent.UNKNOWN

        return intent

