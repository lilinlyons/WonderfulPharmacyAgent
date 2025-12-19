from agents.agent_utils.session_state import (
    get_conversation_context,
    set_user_message,
    set_agent_message,
)
from agents.agent_utils.rephrase_question import rephrase_with_session_context


class ContextAgent:
    """
    Handles contextual message rephrasing using previous session messages.
    Uses both previous user message and agent response for better context.
    """

    def __init__(self, client, logger):
        self.client = client
        self.logger = logger

    def process(self, session_id: str, user_message: str, user_id) -> str:
        """
        Rephrase user message using previous user message AND agent response.

        Args:
            session_id: Session identifier
            user_message: Current user message
            user_id: User identifier for logging

        Returns:
            Rephrased user message with resolved references
        """
        # Get full conversation context (both user and agent messages)
        session_context = get_conversation_context(session_id)

        prev_user_msg = session_context.get("user_message")
        prev_agent_msg = session_context.get("agent_message")

        self.logger.info("=" * 70)
        self.logger.info("CONTEXT AGENT - Processing message")
        self.logger.info("=" * 70)
        self.logger.info("Current user message: %s", user_message)
        self.logger.info("Previous user message: %s", prev_user_msg)
        self.logger.info("Previous agent message: %s", prev_agent_msg)

        try:
            # Only rephrase if there's previous context
            if prev_user_msg or prev_agent_msg:
                self.logger.info("Previous context found - rephrasing with context")

                rephrased_message = rephrase_with_session_context(
                    self.client,
                    user_message,
                    session_context,
                    user_id
                )

                if rephrased_message != user_message:
                    self.logger.info("✓ Message rephrased successfully")
                    self.logger.info("  Original: %s", user_message)
                    self.logger.info("  Rephrased: %s", rephrased_message)
                    user_message = rephrased_message
                else:
                    self.logger.info("Message was already clear - no changes needed")
            else:
                self.logger.info("No previous context available - using message as-is")

        except Exception as e:
            self.logger.exception("Rephrasing failed: %s", str(e))
            self.logger.warning("Falling back to original message")

        # Store current user message for next turn
        self.logger.info("Storing user message for next turn")
        set_user_message(session_id, user_message)

        self.logger.info("=" * 70)
        return user_message