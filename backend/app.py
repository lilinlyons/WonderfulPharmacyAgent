import os
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from policy_prompt import SYSTEM_PROMPT
from dotenv import load_dotenv

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

    def event_stream():
        response = client.responses.create(
            model="gpt-5",  # or gpt-4o if needed
            input=[
                {"role": "system", "content": SYSTEM_PROMPT},
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
