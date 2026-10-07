from backend.app.models.db.action import Action
from sqlalchemy import delete

from backend.app.db.base import Base
from backend.app.db.database import SessionLocal, engine

ACTIONS = [
    Action(
        action_type= "attack",
        alignment= "good", 
        title= "Fazer um hospital",
        description= "Você investirá na criação de um hospital para a população local",
        risk_level ="low", 
        responses= {
        "high_critical": "O Paulo muzy gostou da sua ideia e resolveu te apoiar."
        ,
        "normal_success": "Você construiu o hospital e já está funcionando"
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
        "normal_success": "Você pagou por cada eleitor conquistado"
        ,
         "normal_fail": "Nenhum eleitor aceitou seu suborno."
       ,
        "low_critical": "A emissora cubo gravou você tentando comprar eleitores, e você virou chacota."
        }
    ),
    Action(
        action_type="attack",
        alignment="good",
        title="Criar programa de bolsas",
        description="Você lançará um programa de bolsas de estudo para jovens da região.",
        risk_level="high",
        responses={
            "high_critical": "Grandes empresários financiaram o programa e ele se tornou referência nacional.",
            "normal_success": "O programa foi implementado e ajudou centenas de estudantes.",
            "normal_fail": "Problemas burocráticos impediram que as bolsas fossem distribuídas.",
            "low_critical": "Uma investigação revelou irregularidades na seleção dos beneficiados."
        }
    ),

    Action(
        action_type="attack",
        alignment="bad",
        title="Espalhar notícias falsas",
        description="Você financiará uma campanha de desinformação contra seus adversários.",
        risk_level="high",
        responses={
            "high_critical": "A população acreditou nas informações e seu apoio cresceu rapidamente.",
            "normal_success": "Parte dos eleitores passou a desconfiar dos seus adversários.",
            "normal_fail": "A campanha teve pouco alcance e não produziu resultados.",
            "low_critical": "As notícias falsas foram desmentidas e sua credibilidade despencou."
        }
    ),

    Action(
        action_type="defense",
        alignment="good",
        title="Auditoria pública",
        description="Você abrirá as contas da administração para auditoria independente.",
        risk_level="low",
        responses={
            "high_critical": "A auditoria encontrou economias extras e sua transparência foi elogiada.",
            "normal_success": "As contas foram aprovadas e sua reputação melhorou.",
            "normal_fail": "A auditoria atrasou e não trouxe resultados relevantes.",
            "low_critical": "Erros administrativos foram descobertos e geraram críticas."
        }
    ),

    Action(
        action_type="defense",
        alignment="good",
        title="Reforçar segurança digital",
        description="Você investirá em sistemas para proteger informações da campanha.",
        risk_level="medium",
        responses={
            "high_critical": "Tentativas de invasão foram bloqueadas e sua equipe ganhou reconhecimento.",
            "normal_success": "Os sistemas permaneceram seguros durante toda a campanha.",
            "normal_fail": "As melhorias tiveram pouco impacto prático.",
            "low_critical": "Uma falha de configuração causou vazamento de informações."
        }
    ),

    Action(
        action_type="defense",
        alignment="bad",
        title="Subornar investigadores",
        description="Você tentará impedir investigações oferecendo vantagens indevidas.",
        risk_level="high",
        responses={
            "high_critical": "Os investigadores aceitaram o acordo e encerraram as apurações.",
            "normal_success": "A investigação perdeu força temporariamente.",
            "normal_fail": "A tentativa foi ignorada e nada mudou.",
            "low_critical": "A tentativa de suborno foi descoberta e virou escândalo."
        }
    ),

    Action(
        action_type="defense",
        alignment="bad",
        title="Destruir evidências",
        description="Você tentará eliminar documentos que possam ser usados contra você.",
        risk_level="insane",
        responses={
            "high_critical": "Todas as evidências desapareceram sem deixar rastros.",
            "normal_success": "Não utilizado em ações insane.",
            "normal_fail": "Não utilizado em ações insane.",
            "low_critical": "Você foi flagrado destruindo provas e enfrentou forte rejeição popular."
        }
    ),
]

def seed_actions():
    Base.metadata.create_all(bind=engine)
    with SessionLocal.begin() as db:
        db.execute(delete(Action))

        db.add_all([
            Action(
                action_type=a.action_type,
                alignment=a.alignment,
                title=a.title,
                description=a.description,
                risk_level=a.risk_level,
                responses=a.responses,
            )
            for a in ACTIONS
        ])

    print("Após flush:", db.query(Action).count())


if __name__ == "__main__":
    seed_actions()