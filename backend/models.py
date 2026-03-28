from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str
    conversation_history: list = []
    user_location: str = ""
    user_lat: float = None
    user_lng: float = None


class ChatResponse(BaseModel):
    reply: str
    resources_cited: list = []
