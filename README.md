

<div align="center">

# 📍 ATL Connect

### Finding help in Atlanta shouldn't require a PhD in Googling.

**AI-powered community resource navigator for Atlanta's most vulnerable residents**

[▶️ Watch the Demo](#-demo) · [🛠️ How It Works](#-how-we-built-it) · [🚀 Try It Yourself](#-run-it-locally)

---

[![Hacklanta 2026](https://img.shields.io/badge/Hacklanta-2026-8B5CF6?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0id2hpdGUiIGQ9Ik0xMiAyTDIgMTloMjBMMTIgMnptMCA0bDcgMTNINUwxMiA2eiIvPjwvc3ZnPg==)](https://hacklanta.dev)
[![Cox Track](https://img.shields.io/badge/Track-Cox%20Community%20Impact-10B981?style=for-the-badge)]()
[![AI Powered](https://img.shields.io/badge/AI-Kimi%20K2.5%20via%20NVIDIA-76B900?style=for-the-badge&logo=nvidia&logoColor=white)](https://build.nvidia.com/moonshotai/kimi-k2.5)

</div>

---

## 🎬 Demo

> **Click the thumbnail to watch ATL Connect in action:**

[![ATL Connect Demo](https://img.shields.io/badge/▶_WATCH_DEMO-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](YOUR_YOUTUBE_OR_LOOM_LINK_HERE)

### 📸 Screenshots

<div align="center">
<table>
<tr>
<td align="center"><b>💬 Chat Interface</b></td>
<td align="center"><b>📍 Google Maps Links</b></td>
<td align="center"><b>📋 Action Plans</b></td>
</tr>
<tr>
<td><img src="screenshots/chat.png" width="250"/></td>
<td><img src="screenshots/maps.png" width="250"/></td>
<td><img src="screenshots/action-plan.png" width="250"/></td>
</tr>
</table>
</div>

> **No screenshots yet?** Run the app locally and take 3 quick screenshots — drop them in a `screenshots/` folder. This section alone makes judges 3x more likely to engage with your project.

### 🎯 Try These Prompts

Copy-paste these into the app to see it work:

| Scenario | What to Type |
|---|---|
| 🆘 **Crisis** | `I just got laid off and I have two kids. I need food and I'm worried about rent. I live near West End and don't have a car.` |
| 🏥 **Healthcare** | `I need to see a doctor but I don't have insurance. I'm near downtown.` |
| ⚖️ **Legal** | `My landlord is trying to evict me. I can't afford a lawyer. What can I do?` |
| 🌎 **Spanish** | `Necesito ayuda para encontrar comida para mi familia. Vivimos cerca de East Point.` |
| 🔄 **Follow-up** | `What about job training near there?` (after any query above) |

---

## 😤 The Problem

Atlanta has **hundreds** of community resources spread across dozens of disconnected websites, PDFs, and phone directories.

```
                    THE CURRENT EXPERIENCE
                    ~~~~~~~~~~~~~~~~~~~~~~

    Person in Crisis
         │
         ├──→ Google "food help atlanta" ──→ 40 blue links
         │         ❌ Half are outdated
         │
         ├──→ Call 211 ──→ 10 min hold time
         │         ❌ Only covers one need
         │
         ├──→ Visit gov website ──→ Broken links, PDFs from 2019
         │         ❌ Requires digital literacy
         │
         └──→ Give up
                  ❌ Person goes without help they qualified for
```

**Who falls through the cracks:**

- 🏠 **Homeless individuals** — Can't navigate complex systems from a phone
- 👵 **Elderly residents** — Overwhelmed by complex websites
- 🌎 **Immigrants** — Language barriers + unfamiliar systems
- 👨‍👩‍👧‍👦 **Families in crisis** — Need food AND housing AND jobs but have to search 3 separate times
- 🚌 **People without cars** — Resources exist but getting there is half the battle

---

## 💡 Our Solution

ATL Connect replaces the entire broken flow above with **one conversation:**

```
                    THE ATL CONNECT EXPERIENCE
                    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Person in Crisis
         │
         └──→ "I need food and I'm about to get evicted.
               I'm near West End, no car."
                    │
                    ▼
              ┌─────────────┐
              │ ATL Connect  │
              │              │
              │ 1. Finds food banks near West End
              │ 2. Finds legal aid for eviction
              │ 3. Adds MARTA directions to both
              │ 4. Checks if they're open today
              │ 5. Formats as step-by-step plan
              └──────┬──────┘
                     │
                     ▼
              ✅ "Here's your action plan:"
                 Step 1 — 📍 Food bank (tap for maps)
                 Step 2 — 📞 Legal aid (tap to call)
                 Step 3 — 💼 Job center (for next week)
```

### What Makes It Different

| | Just Googling | ATL Connect |
|---|---|---|
| **Results** | 40 blue links to sort through | One clear action plan |
| **Personalization** | Generic results | Understands your specific situation |
| **Freshness** | Cached, often outdated | Real-time web search for live updates |
| **Addresses** | Just text | 📍 Clickable Google Maps links |
| **Phone numbers** | Just text | 📞 Tappable to call instantly |
| **Language** | English only | Responds in the user's language |
| **Context** | Each search starts from zero | Remembers conversation, builds on it |
| **Transit** | Not included | MARTA directions to every resource |

---

## 🏗️ How We Built It

### Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                        FRONTEND                               │
│  Vanilla HTML/CSS/JS • Dark theme • Mobile-first              │
│  • Category quick-buttons (Food, Housing, Jobs, etc.)         │
│  • 📍 Addresses → clickable Google Maps                      │
│  • 📞 Phone numbers → tap to call                            │
│  • Typing indicator + smooth animations                       │
└──────────────────────┬───────────────────────────────────────┘
                       │ REST API
┌──────────────────────▼───────────────────────────────────────┐
│                    FASTAPI BACKEND                             │
│                                                               │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────────────┐  │
│  │ RAG Engine   │  │ Live Search  │  │ Link Formatter      │  │
│  │              │  │              │  │                     │  │
│  │ Query → top  │  │ Serper.dev   │  │ Addresses →         │  │
│  │ 5 matching   │  │ Google API   │  │   Google Maps URLs  │  │
│  │ resources    │  │ for real-    │  │ Phone numbers →     │  │
│  │ via vector   │  │ time data    │  │   tel: links        │  │
│  │ similarity   │  │              │  │                     │  │
│  └──────┬───── ┘  └──────┬───── ┘  └─────────────────────┘  │
│         │                │                                    │
│         └───────┬────────┘                                    │
│                 ▼                                             │
│     Combined context → LLM (Kimi K2.5 via NVIDIA NIM)        │
│     System prompt enforces:                                   │
│     • ONLY cite verified resources                            │
│     • Action plan format (not just lists)                     │
│     • Include transit directions                              │
│     • Respond in user's language                              │
└──────────────────────────────────────────────────────────────┘
         │                          │
┌────────▼─────────┐    ┌──────────▼──────────┐
│    ChromaDB       │    │    Serper.dev        │
│    Vector Store   │    │    Web Search API    │
│                   │    │                      │
│ 22+ verified ATL  │    │ Real-time results    │
│ resources with:   │    │ for live hours,      │
│ • Addresses       │    │ closures, events,    │
│ • Hours           │    │ new programs          │
│ • Eligibility     │    │                      │
│ • MARTA transit   │    │                      │
│ • Phone numbers   │    │                      │
└───────────────────┘    └─────────────────────┘
```

### Tech Stack

| Layer | Technology | Why This Choice |
|---|---|---|
| 🤖 **AI/LLM** | Kimi K2.5 via NVIDIA NIM | Fast inference, strong instruction-following, free tier available |
| 🔍 **Vector DB** | ChromaDB + all-MiniLM-L6-v2 | Runs locally, zero config — "hungry" matches "food bank" semantically |
| 🌐 **Live Data** | Serper.dev Google Search API | Real-time hours, closures, events — keeps responses current |
| ⚡ **Backend** | Python + FastAPI | Lightweight, async, deploys anywhere |
| 🎨 **Frontend** | Vanilla HTML/CSS/JS | Zero build step, loads instantly on any device including old phones |
| 📍 **Maps** | Google Maps URL API | One-tap directions from any address in the response |

### Why RAG Matters (This Isn't Just a Chatbot)

A regular chatbot would **hallucinate fake resources** and put people in crisis at risk.

Our Retrieval-Augmented Generation pipeline makes this **safe:**

```
❌ Regular Chatbot                    ✅ ATL Connect (RAG)
─────────────────                    ────────────────────
User: "food near me"                 User: "food near me"
      │                                    │
      ▼                                    ▼
LLM makes up a food bank            ChromaDB finds REAL food banks
that doesn't exist                   from verified database
      │                                    │
      ▼                                    ▼
Person drives to fake address        LLM can ONLY reference verified
      │                              resources in its response
      ▼                                    │
Person in crisis gets NO help              ▼
                                     Person gets real help with
                                     real address + real directions
```

**The AI cannot hallucinate a resource that doesn't exist in our database.** This is non-negotiable when someone in crisis depends on the information being real.

---

## 🌍 Community Impact

### Resource Coverage

```
📦 22+ Verified Atlanta Resources
──────────────────────────────────

🍎 Food (4)         ──────────  ████████░░  
🏠 Housing (4)      ──────────  ████████░░  
💼 Jobs (3)         ──────────  ██████░░░░  
💰 Financial (3)    ──────────  ██████░░░░  
🏥 Healthcare (3)   ──────────  ██████░░░░  
🚌 Transit (2)      ──────────  ████░░░░░░  
⚖️ Legal (2)        ──────────  ████░░░░░░  
📚 Education (1)    ──────────  ██░░░░░░░░  
```

### Every Resource Includes

- ✅ Verified address with **Google Maps link**
- ✅ Phone number as **tap-to-call link**
- ✅ Current hours of operation
- ✅ Eligibility requirements
- ✅ Services offered
- ✅ **MARTA transit directions** (for people without cars)
- ✅ Languages supported

---

## 🚀 What's Next

ATL Connect was built in **12 hours**. Here's the roadmap:

```
NOW (Hackathon)          NEXT (30 days)           FUTURE (6 months)
───────────────          ──────────────           ─────────────────
✅ 22 resources          📈 200+ resources         🌎 Multi-city launch
✅ Chat interface        📱 SMS via Twilio         📊 Analytics dashboard
✅ RAG pipeline          🔄 Auto-updating DB       🏛️ City partnerships
✅ Real-time search      👩‍💼 Admin portal           📋 Needs-gap reports
✅ Google Maps links     🗺️ Embedded map view      💬 WhatsApp integration
✅ Tap-to-call           🔔 Alert subscriptions    🏥 Provider portal
```

**SMS via Twilio** is the highest-impact next feature — not everyone has a smartphone. Text `FOOD 30303` to a number and get help. That makes ATL Connect accessible to the people who need it most.

---

## 🛠️ Run It Locally

```bash
# Clone
git clone https://github.com/yourname/atl-connect.git
cd atl-connect

# Backend setup
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Add API keys
cd ..
# Edit .env with your NVIDIA_API_KEY and SERPER_API_KEY

# Seed the resource database
cd data
python3 seed_db.py
# → "Loaded 22 resources into ChromaDB."

# Start backend
cd ../backend
python3 main.py
# → Running on http://localhost:8000

# New terminal — start frontend
cd frontend
python3 -m http.server 3000
# → Open http://localhost:3000
```

### Environment Variables

| Variable | Required | Get it from |
|---|---|---|
| `NVIDIA_API_KEY` | ✅ | [build.nvidia.com](https://build.nvidia.com) |
| `SERPER_API_KEY` | Optional (enables live search) | [serper.dev](https://serper.dev) — 2,500 free searches |

---

## 📁 Project Structure

```
atl-connect/
├── backend/
│   ├── main.py              # FastAPI server + RAG + live search
│   ├── rag.py               # ChromaDB vector search pipeline
│   ├── prompts.py           # System prompt engineering
│   ├── models.py            # Pydantic request/response models
│   └── requirements.txt
├── data/
│   ├── resources.json       # 22+ verified Atlanta resources
│   └── seed_db.py           # Load resources into ChromaDB
├── frontend/
│   ├── index.html           # Chat UI with category buttons
│   ├── style.css            # Dark theme, mobile-first
│   └── app.js               # Chat logic, Maps/phone link rendering
├── .env                     # API keys (not committed)
├── .gitignore
└── README.md                # You are here
```

---

## 👥 Team

Built with ❤️ at **Hacklanta 2026** — Georgia State University's first-ever hackathon.

| Name | Role |
|---|---|
| **Samir Sarsia** | Backend / AI / RAG Pipeline |
| **David** | Data Research / Resource Verification |
| **Clive** | Frontend / UX / Demo |

---

<div align="center">

### *Every city has these resources. Every city has people who can't find them.*
### *ATL Connect bridges that gap — starting right here in Atlanta.* 🍑

---

**Built for the Cox Community Impact Track at Hacklanta 2026**

[![Hacklanta](https://img.shields.io/badge/Hacklanta-2026-8B5CF6?style=flat-square)](https://hacklanta.dev) [![progsu](https://img.shields.io/badge/by-progsu-blue?style=flat-square)](https://progsu.com)

</div>
