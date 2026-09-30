from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.api.deps import get_db
from backend.app.schemas.db.party import PartyResponse
from backend.app.services.db.party_service import get_parties


router_party = APIRouter()


@router_party.get(
    "/parties",
    response_model=list[PartyResponse]
)
def get_parties_route(
    db: Session = Depends(get_db)
):
    return get_parties(db)