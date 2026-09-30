from pydantic import BaseModel


class PartyResponse(BaseModel):
    id: str
    name: str
    color: str

    class Config:
        from_attributes = True