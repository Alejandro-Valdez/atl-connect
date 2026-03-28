import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import anthropic

from models import ChatRequest, ChatResponse
from rag import get_relevant_resources, get_all_resources
from prompts import SYSTEM_PROMPT

load_dotenv()

app = FastAPI(title="ATL Connect")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    # 1 — Retrieve relevant resources via RAG
    relevant_resources = get_relevant_resources(req.message)

    # 2 — Format resource context
    resource_context = "\n\n".join(
        f"**{r['name']}**\n"
        f"Category: {r['category']}\n"
        f"Address: {r['address']}\n"
        f"Phone: {r['phone']}\n"
        f"Hours: {r['hours']}\n"
        f"Services: {r['services']}\n"
        f"Eligibility: {r['eligibility']}\n"
        f"Transit: {r.get('transit_access', 'N/A')}\n"
        f"Description: {r['description']}"
        for r in relevant_resources
    )

    # 3 — Build messages
    messages = list(req.conversation_history)

    location_line = (
        f"User's location: {req.user_location}\n" if req.user_location else ""
    )

    messages.append({
        "role": "user",
        "content": (
            f"User's question: {req.message}\n\n"
            f"{location_line}"
            f"Here are the relevant Atlanta community resources I found:\n\n"
            f"{resource_context}\n\n"
            f"Use ONLY these resources in your response. "
            f"Do not make up any resources."
        ),
    })

    # 4 — Call Claude
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=messages,
    )

    reply = response.content[0].text

    return ChatResponse(
        reply=reply,
        resources_cited=[r["name"] for r in relevant_resources],
    )


@app.get("/resources")
def list_resources(category: str = None):
    """Browse all resources, optionally filtered by category."""
    resources = get_all_resources()
    if category:
        resources = [
            r for r in resources
            if category.lower() in r.get("category", "").lower()
        ]
    return {"resources": resources}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
