class PartyValidator:

    def not_exist(self, party):
        if party is None:
            raise ValueError("Partido não existe")

        return party