class PendingActionValidator:
    def pending_action_exist(self,pending_action):
        if pending_action is None:
            raise ValueError("Não existe pergunta pendente para essa ação")
    def verify_pending_action_player_id(self,pending_action,player_id):
        if pending_action["player_id"] != player_id:
            raise ValueError("Essa pergunta não pertence a esse jogador")
        