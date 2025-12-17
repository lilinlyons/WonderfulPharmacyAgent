from utils.session_state import get_prev_message, set_prev_message
from utils.rephrase_question import rephrase_with_context

class ContextAgent:
    """
    Handles contextual message rephrasing using previous session messages.
    """

    def __init__(self, client, logger):
        self.client = client
        self.logger = logger

    def process(self, session_id: str, user_message: str, user_id) -> str:
        prev_message = get_prev_message(session_id)
        self.logger.info("Prev message: %s", prev_message)

        try:
            if prev_message:
                self.logger.info("Rephrasing with previous context")
                user_message = rephrase_with_context(
                    self.client, user_message, prev_message, user_id
                )
                self.logger.info("Rephrased message: %s", user_message)

        except Exception:
            self.logger.exception("Rephrasing failed")

        set_prev_message(session_id, user_message)

        return user_message
