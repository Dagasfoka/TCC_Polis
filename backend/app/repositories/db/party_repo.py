from sqlalchemy.orm import Session

from backend.app.models.db.party import Party


class PartyRepo:

    def get_all(self, db: Session):
        return db.query(Party).all()

    def get_by_id(
        self,
        db: Session,
        party_id: str
    ):
        return db.get(Party, party_id)