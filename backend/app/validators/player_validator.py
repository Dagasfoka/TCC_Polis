def verify_player_exist(player):
    if player is None:
        raise ValueError("Jogador não encontrado")