import os
from typing import List, Optional
from fastapi import FastAPI
from pydantic import BaseModel
from ai_agent import get_response_from_ai_agent
from chat_storage import save_chat

class RequestState(BaseModel):
    model_name: str
    model_provider: str
    messages: List[str]
    allow_search: bool
    system_prompt: Optional[str] = None

ALLOWED_MODELS = {"llama3-70b-8192", "mixtral-8x7b-32768", "llama-3.3-70b-versatile", "gpt-4o-mini"}
app = FastAPI(title="LangGraph AI Agent")

@app.post("/chat")
def chat_endpoint(request: RequestState):
    """
    API EndPoint to interact with ChatBot using LangGraph and Search Tools.
    It dynamically selects the model specified in the request.
    """

    if request.model_name not in ALLOWED_MODELS:
        return {"error": "Invalid model name. Kindly select a Valid AI Model."}

    prompt = request.system_prompt or "Act as an AI ChatBot who is smart and friendly."
    response = get_response_from_ai_agent(
        request.model_name,
        request.messages,
        request.allow_search,
        prompt,
        request.model_provider,
    )

    save_chat(user_message=request.messages[0], bot_response=response, model=request.model_name)
    return response


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=os.getenv("HOST", "127.0.0.1"), port=int(os.getenv("PORT", "8000")))