from typing import Literal

from pydantic import BaseModel


class RegionalMissionContent(BaseModel):
    region: str
    quantity: int


class MatchMissionContent(BaseModel):
    region: list[RegionalMissionContent] | None = None
    state: list[str] | None = None
    destruction: str | None = None


class MatchMissionSchema(BaseModel):
    match_id: int
    mission_id: int
    type: Literal["region", "state", "destruction"]
    content: MatchMissionContent
    owner_id: str