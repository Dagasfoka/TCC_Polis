from backend.app.gateways.party_gateway import PartyGateway
from backend.app.validators.party_validator import PartyValidator


def get_parties(db):
    party_gateway = PartyGateway()

    return party_gateway.get_all(db)


def get_party(db, party_id):
    party_gateway = PartyGateway()
    party_validator = PartyValidator()

    party = party_gateway.get_by_id(
        db,
        party_id
    )

    return party_validator.not_exist(party)