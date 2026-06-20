from pydantic import BaseModel, Field
from typing import Optional

class QuestBase(BaseModel):
    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    is_active: bool = True

class QuestCreate(QuestBase):
    pass

class QuestUpdate(QuestBase):
    name: Optional[str] = None
    
class QuestResponse(QuestBase):
    id: int

    class Config:
        from_attributes = True
