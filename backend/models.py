from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str
    conversation_history: list = []
    user_location: str = ""


class ChatResponse(BaseModel):
    reply: str
    resources_cited: list = []
