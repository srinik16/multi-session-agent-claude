# Multi-Session Agent (Claude)

A FastAPI service that maintains separate, context-aware conversation sessions per user using the Anthropic Claude API.

## How It Works

Each incoming question is first classified into a topic (e.g. `coding`, `travel`, `finance`) using Claude Haiku. The service then routes the user to a dedicated session for that topic, so conversation history stays focused and relevant. A user can have multiple parallel sessions — one per detected context.

```
POST /ask
  │
  ├─ detect_context(question)  →  e.g. "coding"
  │
  ├─ lookup session[user_id:coding]  (create if new)
  │
  └─ session.ask(question)  →  answer (with full history)
```

## Project Structure

| File | Purpose |
|---|---|
| [main.py](main.py) | FastAPI app with the `/ask` endpoint |
| [session_manager.py](session_manager.py) | Routes users to per-context sessions |
| [context_classifier.py](context_classifier.py) | Classifies questions using Claude Haiku |
| [claude_client.py](claude_client.py) | `ClaudeSession` class — wraps Claude Sonnet with message history |

## Setup

**1. Install dependencies**
```bash
pip install fastapi uvicorn anthropic python-dotenv
```

**2. Configure your API key**

Create a `.env` file:
```
ANTHROPIC_API_KEY=your_api_key_here
```

**3. Run the server**
```bash
uvicorn main:app --reload
```

## Usage

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"user_id": "alice", "question": "What is a binary search tree?"}'
```

**Response:**
```json
{
  "context": "coding",
  "answer": "A binary search tree is..."
}
```

Send a follow-up in the same context and the session remembers the conversation history automatically.

## Why Use This Over a Regular Agent

A standard single-session agent keeps all conversation history in one flat thread. As topics shift, the context window fills with irrelevant history, degrading response quality and increasing token costs. This service solves that with automatic topic routing:

| | Regular Agent | Multi-Session Agent |
|---|---|---|
| **Context isolation** | All topics mixed in one thread | Separate session per topic |
| **History relevance** | Degrades as topics shift | Always focused on current context |
| **Token efficiency** | Pays for unrelated history | Only sends relevant history |
| **Parallel contexts** | Manual session management | Automatic per-user, per-topic routing |
| **Follow-up accuracy** | Confused by topic switches | Picks up exactly where the topic left off |

For example, if Alice asks about binary trees and then asks about flight prices, those conversations are tracked in separate sessions. Switching back to coding picks up the exact coding thread — not a mix of everything.

## Models Used

- **Context classification:** `claude-haiku-4-5` (fast and cheap)
- **Conversation:** `claude-sonnet-4-6` (full responses with history)
