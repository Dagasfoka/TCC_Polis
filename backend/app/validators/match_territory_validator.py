def verify_target_exist(target):
    if target is None:
        raise ValueError("Território não encontrado")
def verify_target_owner(target,player_id):
    if target.get("owner_id") == player_id:
        raise ValueError("Você já controla esse território")