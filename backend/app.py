import os
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from dotenv import load_dotenv
from utils.get_prescriptions_per_user import get_prescription_per_user
from workflows.utils.fetch_users import fetch_users
from bert.labels import Intent
from utils.policy_prompt import SYSTEM_PROMPT
from bert.classifier import classify_intent
from router import route
from utils.rephrase_question import rephrase_with_context
from utils.session_logger import get_session_logger
from utils.session_state import get_prev_message, set_prev_message


load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


@app.post("/chat")
async def chat(req: Request):

    try:
        body = await req.json()
    except Exception:
        return StreamingResponse(
            iter(["Invalid request format."]),
            media_type="text/plain",
        )

    user_message = body.get("message", "").strip()

    session_id = body.get("session_id", "anonymous")
    user_id = body.get("user_id")

    prev_message = get_prev_message(session_id)

    logger = get_session_logger(session_id)
    logger.info("New request received")

    if not user_message:
        logger.warning("Empty user message")
        return StreamingResponse(
            iter(["Please enter a message."]),
            media_type="text/plain",
        )

    logger.info("User message: %s", user_message)
    logger.info("Prev message: %s", prev_message)


    if prev_message:
        try:
            logger.info("Rephrasing with previous context")
            user_message = rephrase_with_context(
                client, user_message, prev_message
            )
            logger.info("Rephrased message: %s", user_message)
        except Exception:
            logger.exception("Rephrasing failed")

    # ALWAYS store the final message for the NEXT request
    set_prev_message(session_id, user_message)

    # Intent classification
    try:
        intent = classify_intent(user_message)
        logger.info("Intent: %s", intent)
    except Exception:
        logger.exception("Intent classification failed")
        intent = Intent.UNKNOWN

    # Routing
    if intent == Intent.UNKNOWN:
        system_context = ""
        user_prompt = (
            "Tell the user politely that you can only help with pharmacy-related "
            "questions such as medications, prescriptions, or availability."
        )
        logger.info("Handled UNKNOWN intent")
    else:
        try:
            handler = route(intent)

            workflow_result = handler(
                user_message,
                user_id=user_id,
            )

            system_context = workflow_result.get("context", "")
            user_prompt = user_message
            logger.info("Workflow executed successfully")
        except Exception:
            logger.exception("Workflow failed")
            system_context = ""
            user_prompt = (
                "Apologize briefly and ask the user to try again."
            )

    def event_stream():
        try:
            response = client.responses.create(
                model="gpt-5",
                input=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "system", "content": system_context},
                    {"role": "user", "content": user_prompt},
                ],
                stream=True,
            )

            for event in response:
                if event.type == "response.output_text.delta" and event.delta:
                    yield event.delta

        except Exception:
            logger.exception("LLM streaming failed")
            yield "Sorry, something went wrong."

        yield ""

    return StreamingResponse(event_stream(), media_type="text/plain")

@app.get("/users")
def get_users():
    """
    Return all users for the frontend user selector
    """
    try:
        users = fetch_users()

        # Adapt fields for frontend expectations
        return [
            {
                "id": user["id"],
                "full_name": user["full_name"],
                "role": user["role"],
                "lang": user["preferred_lang"],
            }
            for user in users
        ]

    except Exception:
        return []

@app.get("/prescription-requests/{user_id}")
def get_prescription_requests(user_id: str):
    return get_prescription_per_user(user_id)

@app.get("/health")
def health():
    return {"ok": True}
