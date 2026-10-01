# Criar sala, entrar, sair, iniciar partida.]
from backend.app.factories.room_factory import RoomFactory
from backend.app.gateways.room_gateways import RoomGateway
from backend.app.validators.room_validators import RoomValidator
from backend.app.validators.player_validators import PlayerValidator
from backend.app.services.redis.match_service import MatchService
from backend.app.gateways.player_gateways import PlayerGateway
from backend.app.services.db.party_service import get_party
import random

class RoomService:
    def __init__(self) -> None:
        self.room_gateway=RoomGateway()
        self.room_factory = RoomFactory()
        self.room_validator = RoomValidator()
        self.player_gateway=PlayerGateway()
        self.player_validator=PlayerValidator()
        self.match_service=MatchService()
    def create_room(self,host_player_id: str,is_private: bool = False) -> dict:
        room_dict = self.room_factory.create_room(
            host_player_id,
            is_private
        )

        room_dict = self.room_validator.not_exist(room_dict)

        return room_dict
    def join_random_room(self,player_id):
        public_rooms = self.room_factory.get_public_rooms()
        
        if public_rooms:
            room = random.choice(public_rooms)
            return self.join_room(
                player_id=player_id,
                room_code=room["room_code"]
            )
        
        return self.create_room(
            host_player_id=player_id,
            is_private=False
        )

    def join_room(self,player_id, room_code):


        room_dict = self.room_gateway.get_room(room_code)
        
        room_dict = self.room_validator.not_exist(room_dict)
        room_dict = self.room_validator.max_players_room(room_dict)
        
        player = self.player_gateway.get_player(player_id)

        player=self.player_validator.not_exist(player)
        player_id=player["player_id"]
        # evitar duplicado
        self.room_validator.player_is_duplicate(player_id,room_dict)

        room_player = self.room_factory.create_room_player(
        player_id
        )

        room_dict["players"][room_player["player_id"]] = {
            "ready": room_player["ready"],
            "host": room_player["host"],
            "party_id": room_player["party_id"],
        }

        self.room_factory.update_room(room_dict)
        
        return room_dict
    def get_room(self,room_code):
        return self.room_gateway.get_room(room_code)

    def start_game(self,db, room_code, player_id):
        room_dict = self.room_gateway.get_room(room_code)
        room_dict = self.room_validator.not_exist(room_dict)

        player_id = self.room_validator.player_can_start(
            player_id,
            room_dict
        )

        if not self.room_validator.ready_to_start(room_dict):
            raise ValueError  ("Nem todos os jogadores estão prontos")

        match = self.match_service.create_match(
            db=db,
            room_code=room_code
        )

        room_dict["status"] = "in_game"
        room_dict["match_id"] = match["match_id"]

        self.room_factory.update_room(room_dict)

        return match
    def put_ready(self,room_code,player_id):
        room_dict = self.room_gateway.get_room(room_code)
        room_dict=self.room_validator.not_exist(room_dict)

        player = self.player_gateway.get_player(player_id)
        player=self.player_validator.not_exist(player)
        player_id=player["player_id"]
        self.room_factory.put_ready(room_dict,player_id)
        self.room_factory.update_room(room_dict)
        return room_dict
    def delete_player(self,room_code,host_id,player_id):
        player = self.player_gateway.get_player(player_id)
        player=self.player_validator.not_exist(player)
        player_id=player["player_id"]    
        
        room_dict = self.room_gateway.get_room(room_code)
        
        room_dict=self.room_validator.not_exist(room_dict)
        room_dict=self.room_validator.can_delete(room_dict,host_id)
        room_dict=self.room_factory.delete_player(room_dict,player_id)
        self.room_factory.update_room(room_dict)
        return room_dict

    def exit_room(self,room_code, player_id):
        # Buscar e validar a sala
        room_dict = self.room_gateway.get_room(room_code)
        room_dict = self.room_validator.not_exist(room_dict)

        # Validar se o jogador pertence à sala
        player_id = self.room_validator.player_in_room(
            room_dict,
            player_id
        )
        
        # Verificar se o jogador é o host
        was_host = self.room_validator.player_is_host(
            room_dict,
            player_id
        )
        
        # Remover o jogador
        room_dict = self.room_factory.delete_player(
            room_dict,
            player_id
        )
        
                # Excluir a sala caso não existam jogadores
        if self.room_validator.room_is_empty(room_dict):
                room_dict=self.room_factory.delete_room(room_code)
                return room_dict
        
        # Transferir a liderança se o host saiu
        if was_host:
                room_dict = self.room_factory.transfer_host(
                    room_dict
                )
        # Salvar a sala atualizada no Redis
        self.room_factory.update_room(room_dict)

        return room_dict
    def change_room_privacy(
        self,
        room_code,
        host_id,
        is_private
    ):
        # Buscar sala
        room_dict = self.room_gateway.get_room(room_code)
        # Verificar se existe
        room_dict = self.room_validator.not_exist(room_dict)
        # Verificar se quem está alterando é o host
        self.room_validator.player_can_start(
            host_id,
            room_dict
        )
        # Alterar privacidade
        room_dict["is_private"] = is_private
        # Salvar no Redis
        self.room_factory.update_room(room_dict)
        return room_dict

    def choose_party(
        self,
        db,
        room_code,
        player_id,
        party_id
    ):

        room_dict = self.room_gateway.get_room(room_code)
        room_dict = self.room_validator.not_exist(room_dict)

        self.room_validator.player_in_room(
            room_dict,
            player_id
        )

        # Verifica se o partido existe no banco
        get_party(db, party_id)

        # Verifica se está disponível nesta sala
        self.room_validator.party_is_available(
            room_dict,
            player_id,
            party_id
        )

        # Registra escolha
        room_dict["players"][player_id]["party_id"] = party_id

        self.room_factory.update_room(room_dict)

        return room_dict