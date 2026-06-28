# Agentic Chatbot — FastAPI + Streamlit + LangGraph

An AI chat application with a Streamlit frontend and a FastAPI backend. The backend runs a LangGraph ReAct agent that can call Groq or OpenAI models, optionally use Tavily web search as a tool, and logs every exchange to a MySQL database.

## Features

- Chat with an AI agent powered by Groq or OpenAI models
- Optional web search via Tavily, used as a tool the agent can call
- Persistent chat logging to MySQL (`chat_history` table)
- Sidebar with session history, new-chat reset, and a message filter
- Simple, single-turn query interface

## Architecture

```
Streamlit (frontend.py)
        |  POST /chat
        v
FastAPI (backend.py)
        |
        +--> LangGraph ReAct agent (ai_agent.py)
        |        |
        |        +--> Groq or OpenAI (LLM inference)
        |        +--> Tavily (optional search tool)
        |
        +--> chat_storage.py --> database.py --> MySQL (chat_history table)
```

The frontend never talks to the database or the LLM providers directly — everything goes through the FastAPI backend.

## Prerequisites

- Python 3.11+
- A running MySQL server (local or remote)
- API keys for [Groq](https://console.groq.com), [OpenAI](https://platform.openai.com/api-keys), and [Tavily](https://app.tavily.com)

## Project structure

| File | Purpose |
|---|---|
| `frontend.py` | Streamlit UI — collects the query, calls the backend, renders the response |
| `backend.py` | FastAPI app exposing `POST /chat` |
| `ai_agent.py` | Builds the LangGraph ReAct agent and calls the selected LLM provider |
| `chat_storage.py` | Inserts each exchange into MySQL |
| `database.py` | MySQL connection helper, reads credentials from `.env` |
| `schema.sql` | Creates the `chatbot_db` database and `chat_history` table |
| `requirements.txt` | Pinned Python dependencies |
| `.env.example` | Template for your local `.env` file (no real secrets) |

## Setup

### 1. Clone and enter the project directory

```bash
git clone <your-repo-url>
cd <your-repo-folder>
```

### 2. Create a Python virtual environment

Choose **one** of the following.

<details>
<summary>Using <code>pip</code> and <code>venv</code> (recommended)</summary>

```bash
python -m venv venv
```

Activate it:

```bash
# macOS/Linux
source venv/bin/activate

# Windows (PowerShell)
venv\Scripts\Activate.ps1
```

</details>

<details>
<summary>Using Pipenv</summary>

```bash
pip install pipenv
pipenv install -r requirements.txt
pipenv shell
```

</details>

<details>
<summary>Using Conda</summary>

```bash
conda create --name agentic-chatbot python=3.11
conda activate agentic-chatbot
```

</details>

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up the database

Create the database and table using the provided schema:

```bash
mysql -u root -p < schema.sql
```

This creates a `chatbot_db` database with a `chat_history` table. Adjust the user/host if your MySQL setup differs.

### 5. Configure environment variables

Copy the example file and fill in your real credentials:

```bash
cp .env.example .env
```

Then edit `.env`:

```env
GROQ_API_KEY=your_groq_api_key
OPENAI_API_KEY=your_openai_api_key
TAVILY_API_KEY=your_tavily_api_key

DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_db_password
DB_NAME=chatbot_db
```

> **Security note:** `.env` holds live secrets. It's already excluded via `.gitignore` — never commit it, and rotate any key that's ever been pasted somewhere public (chat logs, screenshots, repos).

## Running the app

The backend and frontend run as two separate processes — start the backend first.

**Terminal 1 — start the backend:**

```bash
python backend.py
```

The API will be available at `http://127.0.0.1:8000`.

**Terminal 2 — start the frontend:**

```bash
streamlit run frontend.py
```

Streamlit will print a local URL (typically `http://localhost:8501`) — open it in your browser.

> **Important:** Keep the backend running in its own terminal the whole time you're using the app. If it's not running, the frontend's requests to `/chat` will fail.

## Using the app

1. Choose a provider (Groq or OpenAI) and a model from the dropdown.
2. Optionally enable **Allow Web Search** to let the agent call Tavily for up-to-date information.
3. Type your question and click **Ask Agent!**
4. The response appears below, and the exchange is saved to your session sidebar and to MySQL.

## Available models

| Provider | Models |
|---|---|
| Groq | `llama-3.3-70b-versatile`, `mixtral-8x7b-32768` |
| OpenAI | `gpt-4o-mini` |

## Notes & limitations

- The sidebar history is **session-only** — it resets when Streamlit restarts. Persistent history exists in MySQL, but the frontend doesn't yet read it back; that's a natural next step if you want history to survive restarts.
- Each request currently sends a single message (no multi-turn conversational memory is passed back to the agent).
- `backend.py` validates `model_name` against an allow-list before invoking the agent, so unsupported model names return a clean error instead of failing deep in the agent.

## Troubleshooting

| Symptom | Likely cause |
|---|---|
| `Request failed: 500` in the UI | Backend isn't running, or an API key is missing/invalid — check the backend terminal for the traceback |
| `GROQ_API_KEY is missing` on startup | `.env` wasn't created, or the key name doesn't match exactly |
| MySQL connection error | MySQL isn't running, or `DB_HOST`/`DB_USER`/`DB_PASSWORD`/`DB_NAME` don't match your server |
| `Invalid model name` error | The model you selected isn't in the backend's `ALLOWED_MODELS` set — add it there if you need a new model |

## License

Add your preferred license here (e.g. MIT).
