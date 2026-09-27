import os

from fastapi import FastAPI, HTTPException
from openai import OpenAI
from pydantic import BaseModel, Field

app = FastAPI()

# Reads OPENAI_API_KEY from your environment. Never put the key in this file.
client = OpenAI()


class PromptRequest(BaseModel):
    text: str = Field(..., min_length=1)


@app.get("/")
def read_root():
    return {"message": "Hello, Germs"}


@app.post("/ask")
def ask_ai(request: PromptRequest):
    if not os.getenv("OPENAI_API_KEY"):
        raise HTTPException(
            status_code=500,
            detail="Set the OPENAI_API_KEY environment variable first.",
        )

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": request.text},
            ],
        )
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    reply = completion.choices[0].message.content
    return {"reply": reply}
