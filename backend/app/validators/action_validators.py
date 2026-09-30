class ActionValidator:
    def action_exist(self,action):  
        if action is None:
            raise ValueError("Ação inválida")
        return action