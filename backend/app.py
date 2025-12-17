import os

import time
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from dotenv import load_dotenv

from agents.context_agent import ContextAgent
from agents.execution_agent import ExecutionAgent
from agents.intent_agent import IntentAgent
from utils.get_prescriptions_per_user import get_prescription_per_user
from utils.get_support_per_user import get_support_per_user
from workflows.utils.fetch_users import fetch_users
from bert.labels import Intent
from utils.policy_prompt import SYSTEM_PROMPT
from utils.logging_utils.session_logger import get_session_logger


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


    logger = get_session_logger(session_id, user_id)
    logger.info("New request received")

    if not user_message:
        logger.warning("Empty user message")
        return StreamingResponse(
            iter(["Please enter a message."]),
            media_type="text/plain",
        )

    logger.info("User message: %s", user_message)
    print(ContextAgent(client, logger).process(session_id, user_message, user_id))

    user_message = ContextAgent(client, logger).process(session_id, user_message, user_id)
    print("user message:",user_message)

    try:
        intent = IntentAgent(logger).process(user_message, user_id)
    except Exception:
        logger.exception("Intent classification failed")
        intent = Intent.UNKNOWN

    if intent == Intent.UNKNOWN:
        system_context = ""
        user_prompt = (
            "Tell the user politely that you can only help with pharmacy-related "
            "questions such as medications, prescriptions, or availability."
        )
        logger.info("Handled UNKNOWN intent")
    else:
        try:
            user_prompt, system_context = ExecutionAgent(logger, intent).execute(user_message, user_id)
            print("user prompt:", user_prompt)
            print("system_cotext", system_context)
            logger.info("Workflow executed successfully")
        except Exception:
            logger.exception("Workflow failed")
            system_context = ""
            user_prompt = (
                "Apologize briefly and ask the user to try again."
            )

    def event_stream():
        start_time = time.monotonic()
        timeout_seconds = 60

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
                # timeout check
                if time.monotonic() - start_time > timeout_seconds:
                    logger.error("LLM streaming timed out after 20 seconds")
                    yield " Sorry, the request timed out. Please try again."
                    return

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

@app.get("/support-requests/{user_id}")
def get_support_requests(user_id: str):
    return get_support_per_user(user_id)

@app.get("/health")
def health():
    return {"ok": True}
