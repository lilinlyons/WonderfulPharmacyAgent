"""
Rephrase user questions by resolving ambiguous pronouns using conversation context
"""

from openai import OpenAI
from utils.logging_utils.workflow_logger import get_workflow_logger


def rephrase_with_context(
    client: OpenAI,
    current_message: str,
    previous_user_message: str | None = None,
    previous_agent_message: str | None = None,
    user_id: str | None = None
) -> str:
    """
    Rephrase user message by resolving ambiguous pronouns (it, that, this, they, etc.)
    using previous user message and agent response for context.
    """
    logger = get_workflow_logger(user_id)

    if not previous_user_message and not previous_agent_message:
        return current_message

    # Truncate long messages to avoid token overflow
    max_length = 300
    prev_user = previous_user_message[-max_length:] if previous_user_message and len(previous_user_message) > max_length else previous_user_message
    prev_agent = previous_agent_message[-max_length:] if previous_agent_message and len(previous_agent_message) > max_length else previous_agent_message

    try:
        context = ""
        if prev_agent:
            context += f"Agent's last response:\n{prev_agent}\n\n"
        if prev_user:
            context += f"Your previous question:\n{prev_user}\n\n"

        logger.info(f"Rephrasing: {current_message[:80]}")

        response = client.responses.create(
            model="gpt-5",
            input=[
                {
                    "role": "system",
                    "content": (
                        "You are a question clarifier. Your job is to make unclear or implicit questions explicit "
                        "by resolving ambiguous pronouns, implied context, and implicit intent.\n\n"
                        "RULES:\n"
                        "1. Resolve explicit pronouns (it, that, this, they, them, etc.) by substituting what was mentioned\n"
                        "2. Infer IMPLICIT INTENT from context:\n"
                        "   - If user says 'X is perfect' after asking about a product → they likely want to ORDER it\n"
                        "   - If user mentions a location in previous context → include it in current query if relevant\n"
                        "   - If previous query was about availability/product info → follow-up likely relates to it\n"
                        "3. Add missing context words (location, action verbs, objects) when strongly implied\n"
                        "4. Don't add information not suggested by context - only clarify what's implicit\n"
                        "5. Don't change core meaning, just make it explicit\n"
                        "6. If already clear, return UNCHANGED\n"
                        "7. Output ONLY the rephrased question - no explanations\n\n"
                        "8. If the question is about stock it will almost always be a stock check question\n\n"
                    ),
                },
                {
                    "role": "user",
                    "content": f"{context}Current question:\n{current_message}\n\nResolve pronouns:",
                },
            ],
        )

        rewritten = response.output_text.strip()

        if rewritten and rewritten != current_message:
            logger.info(f"✓ Rephrased: '{current_message}' → '{rewritten}'")

        return rewritten if rewritten else current_message

    except Exception as e:
        logger.warning(f"Rephrase failed: {str(e)}")
        return current_message


def rephrase_with_session_context(
    client: OpenAI,
    current_message: str,
    session_state: dict,
    user_id: str | None = None
) -> str:
    """Wrapper using session state dict"""
    return rephrase_with_context(
        client=client,
        current_message=current_message,
        previous_user_message=session_state.get("user_message"),
        previous_agent_message=session_state.get("agent_message"),
        user_id=user_id
    )