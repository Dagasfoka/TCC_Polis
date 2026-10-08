class RoomNotFoundError(Exception):
    pass


class PlayerAlreadyInRoomError(Exception):
    pass


class RoomFullError(Exception):
    pass


class OnlyHostError(Exception):
    pass


class PlayerNotInRoomError(Exception):
    pass


class RoomNotReadyError(Exception):
    pass


class PartyUnavailableError(Exception):
    pass