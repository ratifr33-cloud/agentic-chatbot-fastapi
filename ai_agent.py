# Step 1: Setup API Keys for GROQ, OPENAI and TAVILY
import os
import warnings
from pathlib import Path

warnings.filterwarnings("ignore", category=Warning)
warnings.simplefilter("ignore")


def load_env_file() -> None:
    env_path = Path(__file__).resolve().parent / ".env"
    if not env_path.exists():
        return

    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def require_env_var(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(
            f"{name} is missing. Set it in your terminal before running the script.\n"
            f"Example in PowerShell: $env:{name}='your-api-key'"
        )
    return value


load_env_file()
GROQ_API_KEY = require_env_var("GROQ_API_KEY")
TAVILY_API_KEY = require_env_var("TAVILY_API_KEY")
OPENAI_API_KEY = require_env_var("OPENAI_API_KEY")

# Step 2: Setup LLM and Tools
# These imports are intentionally deferred so the FastAPI app can start
# without failing during module import.

system_prompt = "Act as an AI ChatBot who is smart and friendly."


def get_response_from_ai_agent(llm_id, query, allow_search, system_prompt, provider):
    try:
        from langchain_groq import ChatGroq
        from langchain_openai import ChatOpenAI
        from langchain_tavily import TavilySearch
        from langgraph.prebuilt import create_react_agent
        from langchain_core.messages.ai import AIMessage
    except Exception as exc:
        raise RuntimeError(
            "AI dependencies could not be imported. Install the requirements and verify your environment."
        ) from exc

    if provider == "Groq":
        llm = ChatGroq(model=llm_id, api_key=GROQ_API_KEY)
    elif provider == "OpenAI":
        llm = ChatOpenAI(model=llm_id, api_key=OPENAI_API_KEY)
    else:
        raise ValueError(f"Unsupported provider: {provider}")

    tools = [TavilySearch(api_key=TAVILY_API_KEY, max_results=2)] if allow_search else []

    agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt=system_prompt,
    )

    state = {"messages": query}
    response = agent.invoke(state)
    messages = response.get("messages")
    ai_messages = [message.content for message in messages if isinstance(message, AIMessage)]
    return ai_messages[-1]