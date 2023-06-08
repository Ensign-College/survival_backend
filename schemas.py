from typing import List, Optional
from pydantic import BaseModel

class CardDetailsBase(BaseModel):
    title: str
    details: str
    picture: Optional[str] = None

class CardDetailsCreate(CardDetailsBase):
    pass
    
class CardDetailsUpdate(CardDetailsBase):
    pass

class CardDetailsInDB(CardDetailsBase):
    id: int
    card_id: int

    class Config:
        orm_mode = True

class CardBase(BaseModel):
    logo_image_url: str
    title: str

class CardCreate(CardBase):
    pass

class CardUpdate(CardBase):
    pass

class CardInDB(CardBase):
    id: int
    card_details: Optional[List[CardDetailsInDB]] = []

    class Config:
        orm_mode = True
