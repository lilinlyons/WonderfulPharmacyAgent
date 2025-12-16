import os
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from policy_prompt import SYSTEM_PROMPT
from dotenv import load_dotenv
from bert.classifier import classify_intent
from router import route

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
    body = await req.json()
    user_message = body.get("message", "")

    intent = classify_intent(user_message)
    print("Intent classified to:", intent)
    handler = route(intent)

    workflow_result = handler(user_message)
    system_context = workflow_result.get("context", "")

    def event_stream():
        print("prompt:", [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "system", "content": system_context},
                {"role": "user", "content": user_message}]
           )
        response = client.responses.create(
            model="gpt-5",
            input=[
                # {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "system", "content": system_context},
                {"role": "user", "content": user_message},
            ],
            stream=True,
        )

        for event in response:
            if (
                event.type == "response.output_text.delta"
                and event.delta is not None
            ):
                yield event.delta

        # final flush
        yield ""

    return StreamingResponse(
        event_stream(),
        media_type="text/plain"
    )


@app.get("/health")
def health():
    return {"ok": True}
