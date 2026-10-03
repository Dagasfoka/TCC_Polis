from backend.app.models.db.action import Action
from sqlalchemy import delete

from backend.app.db.base import Base
from backend.app.db.database import SessionLocal, engine

OPTIONS = [
    Action(
        action_type= "attack",
        alignment= "good", 
        title= "Fazer um hospital",
        description= "Você investirá na criação de um hospital para a população local",
        risk_level ="low", 
        responses= {
        "high_critical": "O Paulo muzy gostou da sua ideia e resolveu te apoiar."
        ,
        "normal_sucess": "Você construiu o hospital e já está funcionando"
        ,
         "normal_fail": "Você contratou pedreiros duvidosos e a obra falhou"
       ,
        "low_critical": "Um grupo de opositores sabotou a obra"
        }
    ),
    Action(
        action_type= "attack",
        alignment= "bad", 
        title= "Comprar eleitores",
        description= "Você sairá na rua comprando voto de eleitores",
        risk_level ="medium", 
        responses= {
        "high_critical": "Você conseguiu ganhar eleitores sem pagar nada."
        ,
        "normal_sucess": "Você pagou por cada eleitor conquistado"
        ,
         "normal_fail": "Nenhum eleitor aceitou seu suborno."
       ,
        "low_critical": "A emissora cubo gravou você tentando comprar eleitores, e você virou chacota."
        }
    ),
]

def seed_actions():
    Base.metadata.create_all(bind=engine)

    with SessionLocal.begin() as db:
        # Apaga todas as ações antigas.
        db.execute(delete(Action))

        options = [
            Action(**options_data)
            for options_data in OPTIONS
        ]

        db.add_all(options)

    print("Ações antigas apagadas.")
    print("Ações de demonstração criadas com sucesso.")


if __name__ == "__main__":
    seed_actions()