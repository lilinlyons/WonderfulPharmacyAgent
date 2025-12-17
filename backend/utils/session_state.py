SESSION_STATE = {}

def get_prev_message(session_id: str):
    return SESSION_STATE.get(session_id)

def set_prev_message(session_id: str, message: str):
    SESSION_STATE[session_id] = message