

class MatchActionFactory:
    def __init__(self) -> None:
        pass
    def distribute_actions(self,actions):
        player_actions = []
        insane_action = 0
        for action in actions:
            if action['risk_level'] == "insane":
                if insane_action == 2:
                    continue
                insane_action +=1
                
            player_actions.append(action)

            if len(player_actions) == 4:
                break
            
        return player_actions