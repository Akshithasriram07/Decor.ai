from pydantic import BaseModel, Field
class WorkerApplicationRequest(BaseModel):
    role: str = Field(min_length=2, max_length=100)
    location: str = Field(min_length=2, max_length=120)
    phone: str = Field(min_length=8, max_length=40)
    experience: str = Field(min_length=1, max_length=100)
    bio: str = Field(min_length=20, max_length=2000)
    portfolio_url: str | None = Field(default=None, max_length=1000)
