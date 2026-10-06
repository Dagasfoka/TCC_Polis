class ActionValidator:
    def action_exist(self,action):  
        if action is None:
            raise ValueError("Ação inválida")
        return action

    def player_have_money_to_action(self,action,player):
        if action['cost'] > player['match_money']:
            raise ValueError(f"{player['username']} você não tem dinheiro suficiente para fazer essa ação.")
        return action