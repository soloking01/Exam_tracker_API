from pydantic import BaseModel
from typing import Optional


class TrackedItemBase(BaseModel):
    title: str
    category: str  
    status: str   
    notes: Optional[str] = None  

class TrackedItemCreate(TrackedItemBase):
    pass


class TrackedItemResponse(TrackedItemBase):
    id: int

    class Config:
        from_attributes = True 