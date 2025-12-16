import os
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from openai import OpenAI

from policy_prompt import SYSTEM_PROMPT

app = FastAPI()
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

@app.post("/chat")
async def chat(req: Request):
    body = await req.json()
    user_message = body.get("message", "")

    def event_stream():
        response = client.responses.create(
            model="gpt-5",
            input=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
            stream=True
        )

        for event in response:
            # Stream text chunks only
            if event.type == "response.output_text.delta":
                yield event.delta

    return StreamingResponse(
        event_stream(),
        media_type="text/plain"
    )


@app.get("/health")
def health():
    return {"ok": True}
