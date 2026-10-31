from datetime import datetime
from pydantic import BaseModel
class DesignResponse(BaseModel):
    id: str
    title: str
    room: str
    style: str
    image: str
    original_image: str | None = None
    prompt: str | None = None
    description: str = ""
    status: str
    is_public: bool
    created_at: datetime
    model_config = {"from_attributes": True}
