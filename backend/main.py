import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from openai import OpenAI

from models import ChatRequest, ChatResponse
from rag import get_relevant_resources, get_all_resources
from search import search_realtime_resources
from prompts import SYSTEM_PROMPT

load_dotenv()

app = FastAPI(title="ATL Connect")

# In production set ALLOWED_ORIGIN to your Vercel URL; defaults to wildcard for local dev.
_allowed_origin = os.getenv("ALLOWED_ORIGIN", "*")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[_allowed_origin] if _allowed_origin != "*" else ["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def seed_on_startup():
    """Seed ChromaDB from resources.json if the collection is empty."""
    from rag import get_collection, load_resources_into_db
    collection = get_collection()
    if collection.count() == 0:
        print("ChromaDB is empty — seeding from resources.json...")
        load_resources_into_db()
        print("Seeding complete.")

client = OpenAI(
    api_key=os.getenv("NVIDIA_API_KEY"),
    base_url="https://integrate.api.nvidia.com/v1",
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    # 1 — Retrieve relevant resources via RAG (local database)
    relevant_resources = get_relevant_resources(req.message)

    # 2 — Fetch real-time results via Serper
    live_results = search_realtime_resources(req.message, req.user_lat, req.user_lng)

    # 3 — Format RAG resource context
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

    # 4 — Format live search context
    live_context = ""
    if live_results:
        live_context = "\n\n**Real-time search results (live Google data):**\n" + "\n\n".join(
            f"- **{r.get('title', '')}**"
            + (f"\n  Address: {r['address']}" if r.get("address") else "")
            + (f"\n  Phone: {r['phone']}" if r.get("phone") else "")
            + (f"\n  Hours: {r['hours']}" if r.get("hours") else "")
            + (f"\n  Rating: {r['rating']}" if r.get("rating") else "")
            + (f"\n  {r.get('snippet', '')}" if r.get("snippet") else "")
            + (f"\n  Website: {r['link']}" if r.get("link") else "")
            for r in live_results
        )

    # 5 — Build messages
    messages = list(req.conversation_history)

    location_line = ""
    if req.user_location:
        location_line = f"User's location: {req.user_location}\n"
    elif req.user_lat and req.user_lng:
        location_line = f"User's coordinates: {req.user_lat}, {req.user_lng} (Atlanta area)\n"

    messages.append({
        "role": "user",
        "content": (
            f"User's question: {req.message}\n\n"
            f"{location_line}"
            f"**Verified local database resources:**\n\n"
            f"{resource_context if resource_context else '(none matched)'}"
            f"{live_context}\n\n"
            f"Use both the local database AND the real-time search results above to give the best answer. "
            f"Format every address as a Google Maps hyperlink: "
            f"[Full Address](https://www.google.com/maps/search/?api=1&query=Full+Address+Atlanta+GA). "
            f"For real-time results without full details, link to their website so the user can verify."
        ),
    })

    # 4 — Call model via OpenRouter
    response = client.chat.completions.create(
        model="moonshotai/kimi-k2.5",
        max_tokens=1024,
        temperature=1.0,
        top_p=1.0,
        messages=[{"role": "system", "content": SYSTEM_PROMPT}] + messages,
        extra_body={"chat_template_kwargs": {"thinking": False}},
    )

    reply = response.choices[0].message.content

    # Collect live results that have an address for map geocoding
    live_resources = [
        {"name": r.get("title", ""), "address": r["address"]}
        for r in live_results
        if r.get("address")
    ]

    return ChatResponse(
        reply=reply,
        resources_cited=[r["name"] for r in relevant_resources],
        live_resources=live_resources,
    )


@app.get("/resources/by-names")
def resources_by_names(names: str = ""):
    """Return full resource objects (with lat/lng) for a comma-separated list of names."""
    if not names:
        return {"resources": []}
    name_list = [n.strip() for n in names.split(",") if n.strip()]
    all_resources = get_all_resources()
    matched = [
        r for r in all_resources
        if r.get("name") in name_list
    ]
    return {"resources": matched}


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
