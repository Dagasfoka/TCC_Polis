from backend.app.repositories.db.party_repo import PartyRepo

class PartyGateway:

    def __init__(self):
        self.party_repository = PartyRepo()

    def get_all(self, db):
        return self.party_repository.get_all(db)

    def get_by_id(self, db, party_id):
        return self.party_repository.get_by_id(
            db,
            party_id
        )