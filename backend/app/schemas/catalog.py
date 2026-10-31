from pydantic import BaseModel

class ProductResponse(BaseModel):
    id: str
    name: str
    category: str
    price: int
    image: str
    description: str
    brand: str
    rating: float
    available: bool
    model_config = {"from_attributes": True}

class WorkerResponse(BaseModel):
    id: str
    name: str
    role: str
    location: str
    rating: float
    jobs: int
    image: str
    phone: str | None = None
    email: str | None = None
    description: str
    available: bool
    model_config = {"from_attributes": True}
