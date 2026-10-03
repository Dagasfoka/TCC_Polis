from backend.app.gateways.db.action_gateway import ActionGateway
from backend.app.models.db.action import Action
from backend.app.models.redis.match_action import MatchAction
import random

DELIMITADOR = 20 #D20
INSANE_ACTION = "insane"
HIGH_ACTION = "high"
MEDIUM_ACTION = "medium"
LOW_ACTION = "low"
GOOD_ALIGNMENT = "good"
BAD_ALIGNMENT = "bad"
INITIAL_MONEY = 2000
INITIAL_INFLUENCE = 300
POSITIVE_CRITICAL = {HIGH_ACTION : (90/100*DELIMITADOR), MEDIUM_ACTION:(85/100*DELIMITADOR),LOW_ACTION:(80/100*DELIMITADOR)}
NEGATIVE_CRITICAL = {HIGH_ACTION : (15/100*DELIMITADOR), MEDIUM_ACTION:(10/100*DELIMITADOR),LOW_ACTION:(5/100*DELIMITADOR)}
SUCCESS_CHANCE = {"attack":
                    {HIGH_ACTION : [(75/100*DELIMITADOR),(80/100*DELIMITADOR)], 
                     MEDIUM_ACTION:[(45/100*DELIMITADOR),(50/100*DELIMITADOR)],
                     LOW_ACTION:[(20/100*DELIMITADOR),(25/100*DELIMITADOR)]},
                  "defense":
                    {HIGH_ACTION : [(80/100*DELIMITADOR),(85/100*DELIMITADOR)], 
                     MEDIUM_ACTION:[(50/100*DELIMITADOR),(55/100*DELIMITADOR)],
                     LOW_ACTION:[(25/100*DELIMITADOR),(30/100*DELIMITADOR)]},
                    }
COST = {INSANE_ACTION : [(5/100*INITIAL_MONEY),(7/100*INITIAL_MONEY)], 
        HIGH_ACTION : [(8/100*INITIAL_MONEY),(12/100*INITIAL_MONEY)], 
        MEDIUM_ACTION:[(18/100*INITIAL_MONEY),(22/100*INITIAL_MONEY)],
        LOW_ACTION:[(23/100*INITIAL_MONEY),(27/100*INITIAL_MONEY)]}

RETURN_INFLUENCE = {
             INSANE_ACTION : [(60/100*INITIAL_INFLUENCE),(70/100*INITIAL_INFLUENCE)],
             HIGH_ACTION : [(35/100*INITIAL_INFLUENCE),(40/100*INITIAL_INFLUENCE)], 
             MEDIUM_ACTION:[(15/100*INITIAL_INFLUENCE),(25/100*INITIAL_INFLUENCE)],
             LOW_ACTION:[(8/100*INITIAL_INFLUENCE),(12/100*INITIAL_INFLUENCE)]}

RETURN_MONEY = {INSANE_ACTION : 8,
                HIGH_ACTION : 4, 
                MEDIUM_ACTION:2,
                LOW_ACTION:1.5}

CORRUPTION = {INSANE_ACTION : 5,
              HIGH_ACTION : 5, 
              MEDIUM_ACTION:5,
              LOW_ACTION:5}


class ActionsFactory:
    def __init__(self) -> None:
        self.actions_gateway=ActionGateway()

    def randomizar_valores(self,valores):
        return random.randint(int(valores[0]), int(valores[1]))

    def get_actions_by_type(self,action_type:str):
        actions = self.actions_gateway.get_actions_by_type(action_type)
        redis_actions = []
        for action in actions:
            cost = self.randomizar_valores(COST[action.risk_level])

            #valores que o usuário irá receber caso funcione a ação
            influence = self.randomizar_valores(RETURN_INFLUENCE[action.risk_level])
            money = int(RETURN_MONEY[action.risk_level] * cost)
            corruption = 0

            if action.alignment == BAD_ALIGNMENT:
                corruption = CORRUPTION[action.risk_level]
                            
            if action.risk_level == INSANE_ACTION:
                redis_action = self.make_action(
                                action=action,
                                cost=cost,
                                influence=influence,
                                money=money,
                                corruption=corruption
                            )
            else:
                positive_critical = POSITIVE_CRITICAL[action.risk_level]
                negative_critial = NEGATIVE_CRITICAL[action.risk_level]
                success_chance = self.randomizar_valores(SUCCESS_CHANCE[action.action_type][action.risk_level])

                redis_action = self.make_action(action = action, 
                                           cost = cost,
                                           influence = influence,
                                           money = money,
                                           corruption = corruption,
                                           positive_critical = positive_critical,
                                           negative_critial = negative_critial,
                                           success_chance = success_chance)
                
            redis_actions.append(redis_action)
        return redis_actions

    def make_action(self,
                    action : Action,
                    cost : int,
                    influence : int,
                    money : int,
                    corruption : int,
                    positive_critical: int | None = None,
                    negative_critical: int | None = None,
                    success_chance: int | None = None,):
        
        match_action = MatchAction(
            action_id=action.action_id,
            action_type=action.action_type,
            alignment=action.alignment,
            title=action.title,
            description=action.description,
            risk_level=action.risk_level,
            responses=action.responses,

            cost=cost,
            influence=influence,
            money=money,
            corruption=corruption,

            positive_critical=positive_critical,
            negative_critical=negative_critical,
            success_chance=success_chance,
        )
        
        return match_action.to_dict() 


    
            