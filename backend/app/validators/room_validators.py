from dataclasses import dataclass

from backend.app.utils.room_exceptions import (
    RoomNotFoundError,
    PlayerAlreadyInRoomError,
    RoomFullError,
    OnlyHostError,
    PlayerNotInRoomError,
    RoomNotReadyError,
    PartyUnavailableError,
)


@dataclass
class RoomValidator:

    def not_exist(self, room_dict):
        if room_dict is None:
            raise RoomNotFoundError(
                "Sala não existe"
            )

        return room_dict


    def player_can_start(
        self,
        player_id,
        room_dict
    ):
        self.player_in_room(
            room_dict,
            player_id
        )

        players = room_dict["players"]

        if players[player_id]["host"] is not True:
            raise OnlyHostError(
                "Apenas o host pode realizar esta ação"
            )

        return player_id


    def player_is_duplicate(
        self,
        player_id,
        room_dict
    ):
        if player_id in room_dict["players"]:
            raise PlayerAlreadyInRoomError(
                "Player já está na sala"
            )

        return room_dict


    def max_players_room(self, room_dict):
        if len(room_dict["players"]) >= 4:
            raise RoomFullError(
                "A sala está cheia"
            )

        return room_dict


    def ready_to_start(self, room_dict) -> bool:
        self.four_players(room_dict)

        players = room_dict["players"]

        for player_id in players:
            player = players[player_id]

            # Todos precisam escolher partido
            if not player.get("party_id"):
                return False

            # Host não precisa dar ready
            if player["host"] is True:
                continue

            if player["ready"] is not True:
                return False

        return True


    def can_delete(
        self,
        room_dict,
        player_id
    ):
        self.player_in_room(
            room_dict,
            player_id
        )

        if self.player_is_host(
            room_dict,
            player_id
        ):
            return room_dict

        raise OnlyHostError(
            "Somente o host pode remover jogadores"
        )


    def player_is_host(
        self,
        room_dict,
        player_id
    ):
        self.player_in_room(
            room_dict,
            player_id
        )

        return (
            room_dict["players"][player_id]["host"]
            is True
        )


    def four_players(self, room_dict):
        if len(room_dict["players"]) != 4:
            raise RoomNotReadyError(
                "A sala precisa ter quatro jogadores"
            )

        return True


    def player_in_room(
        self,
        room_dict,
        player_id
    ):
        if player_id not in room_dict["players"]:
            raise PlayerNotInRoomError(
                "Jogador não está na sala"
            )

        return player_id


    def room_is_empty(self, room_dict):
        return len(room_dict["players"]) == 0


    def validate_ready_to_start(
        self,
        room_dict
    ):
        if not self.ready_to_start(room_dict):
            raise RoomNotReadyError(
                "Nem todos os jogadores estão prontos"
            )

        return room_dict


    def party_is_available(
        self,
        room_dict,
        player_id,
        party_id
    ):
        for other_id, player_data in (
            room_dict["players"].items()
        ):
            if (
                other_id != player_id
                and
                player_data.get("party_id") == party_id
            ):
                raise PartyUnavailableError(
                    "Esse partido já foi escolhido"
                )

        return party_id