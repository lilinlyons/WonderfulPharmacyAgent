from openai import OpenAI
from utils.logging_utils.workflow_logger import get_workflow_logger

def rephrase_with_context(
    client: OpenAI,
    current_message: str,
    previous_message: str | None,
    user_id: str | None = None
) -> str:
    """
    Uses the LLM ONLY to rewrite the user's question by resolving references
    using the previous user message. The LLM must not answer the question.
    """
    logger = get_workflow_logger(user_id)
    if not previous_message:
        return current_message

    try:
        response = client.responses.create(
            model="gpt-5",
            input=[
                {
                    "role": "system",
                    "content": (
                        "You are a question rewriter.\n"
                        "Your task is to rewrite the user's LATEST question ONLY if it is ambiguous.\n\n"
                        "You may receive input embedded inside logs (timestamps, log levels, agent names, etc.).\n"
                        "Ignore all log metadata and extract ONLY:\n"
                        "- The user's latest message\n"
                        "- The immediately previous user message (if present)\n\n"
                        "Use the previous user message ONLY to disambiguate the latest question.\n\n"
                        "RULES:\n"
                        "- Do NOT answer the question\n"
                        "- Do NOT add new information\n"
                        "- Do NOT infer details not present in the messages\n"
                        "- Do NOT give advice or explanations\n"
                        "- Do NOT include timestamps, logs, or agent text in the output\n"
                        "- Keep the result as ONE single clear question\n"
                        "- Preserve the user's intent exactly\n"
                        "- If the latest question is already clear, return it UNCHANGED"
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Previous question:\n{previous_message}\n\n"
                        f"Current question:\n{current_message}\n\n"
                        "Rewrite the current question so it is explicit:"
                    ),
                },
            ],
        )

        rewritten = response.output_text.strip()
        return rewritten if rewritten else current_message

    except Exception:
        logger.exception("Failed to rephrase question with context")
        return current_message
