"""
Session state management that tracks both user and agent messages
"""

SESSION_STATE = {}

def get_session_state(session_id: str):
    """Get full session state (user and agent messages)"""
    if session_id not in SESSION_STATE:
        SESSION_STATE[session_id] = {
            "user_message": None,
            "agent_message": None,
        }
    return SESSION_STATE[session_id]


def get_prev_user_message(session_id: str) -> str | None:
    """Get the last user message from session"""
    state = get_session_state(session_id)
    return state.get("user_message")


def get_prev_agent_message(session_id: str) -> str | None:
    """Get the last agent message from session"""
    state = get_session_state(session_id)
    return state.get("agent_message")


def get_conversation_context(session_id: str) -> dict:
    """Get full conversation context (both user and agent)"""
    state = get_session_state(session_id)
    return {
        "user_message": state.get("user_message"),
        "agent_message": state.get("agent_message"),
    }


def set_user_message(session_id: str, message: str):
    """Store the user's message"""
    state = get_session_state(session_id)
    state["user_message"] = message


def set_agent_message(session_id: str, message: str):
    """Store the agent's message"""
    state = get_session_state(session_id)
    state["agent_message"] = message


def update_session_state(session_id: str, user_message: str = None, agent_message: str = None):
    """Update session state with user and/or agent messages"""
    state = get_session_state(session_id)
    if user_message is not None:
        state["user_message"] = user_message
    if agent_message is not None:
        state["agent_message"] = agent_message


def clear_session(session_id: str):
    """Clear session state"""
    if session_id in SESSION_STATE:
        del SESSION_STATE[session_id]