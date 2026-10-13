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
    Action(
        action_type="attack",
        alignment="good",
        title="Ampliar o transporte público",
        description="Você investirá na expansão do transporte público para melhorar a mobilidade da população.",
        risk_level="medium",
        responses={
            "high_critical": "O projeto recebeu financiamento extra e se tornou referência nacional.",
            "normal_success": "Novas linhas foram implementadas e facilitaram o deslocamento da população.",
            "normal_fail": "Atrasos nas obras impediram a conclusão das melhorias.",
            "low_critical": "Os custos dispararam e a população criticou a má gestão do projeto."
        }
    ),
    Action(
        action_type="attack",
        alignment="good",
        title="Criar centros profissionalizantes",
        description="Você criará centros de formação profissional para ampliar as oportunidades de emprego.",
        risk_level="low",
        responses={
            "high_critical": "Empresas parceiras financiaram os centros e contrataram centenas de alunos.",
            "normal_success": "Os centros começaram a formar profissionais para o mercado de trabalho.",
            "normal_fail": "A falta de equipamentos limitou a oferta de cursos.",
            "low_critical": "Denúncias de favorecimento na seleção dos alunos prejudicaram sua reputação."
        }
    ),
    Action(
        action_type="attack",
        alignment="bad",
        title="Distribuir benefícios em troca de apoio",
        description="Você oferecerá benefícios públicos com o objetivo de conquistar apoio político indevido.",
        risk_level="high",
        responses={
            "high_critical": "Sua estratégia conquistou apoio inesperado, sem gerar suspeitas imediatas.",
            "normal_success": "Parte da população passou a apoiar sua campanha.",
            "normal_fail": "A população rejeitou a proposta e seu apoio não aumentou.",
            "low_critical": "A prática foi denunciada e você passou a ser investigado."
        }
    ),
    Action(
        action_type="attack",
        alignment="bad",
        title="Manipular uma pesquisa eleitoral",
        description="Você financiará a divulgação de uma pesquisa fraudulenta para influenciar a opinião pública.",
        risk_level="insane",
        responses={
            "high_critical": "A divulgação ganhou enorme repercussão e alterou momentaneamente o debate eleitoral.",
            "normal_success": "Não utilizado em ações insane.",
            "normal_fail": "Não utilizado em ações insane.",
            "low_critical": "A fraude foi descoberta, provocando um escândalo e uma queda acentuada de apoio."
        }
    ),
    Action(
        action_type="defense",
        alignment="good",
        title="Publicar prestação de contas",
        description="Você divulgará relatórios detalhados sobre os gastos e resultados da campanha.",
        risk_level="low",
        responses={
            "high_critical": "A transparência recebeu reconhecimento público e fortaleceu sua credibilidade.",
            "normal_success": "A prestação de contas foi aprovada e reduziu as críticas.",
            "normal_fail": "Os relatórios foram publicados, mas não esclareceram todas as dúvidas.",
            "low_critical": "Inconsistências nos relatórios geraram questionamentos públicos."
        }
    ),
    Action(
        action_type="defense",
        alignment="good",
        title="Reforçar a equipe jurídica",
        description="Você contratará especialistas para revisar decisões e prevenir problemas legais.",
        risk_level="medium",
        responses={
            "high_critical": "A equipe identificou um problema grave a tempo e evitou uma crise.",
            "normal_success": "A revisão jurídica reduziu os riscos de novas contestações.",
            "normal_fail": "A equipe não encontrou soluções para os problemas existentes.",
            "low_critical": "Uma orientação equivocada agravou a situação jurídica."
        }
    ),
    Action(
        action_type="defense",
        alignment="bad",
        title="Transferir a culpa para aliados",
        description="Você tentará atribuir a aliados a responsabilidade por irregularidades da sua administração.",
        risk_level="high",
        responses={
            "high_critical": "Seus aliados assumiram a responsabilidade e as suspeitas sobre você diminuíram temporariamente.",
            "normal_success": "Parte das críticas foi direcionada a outros integrantes da equipe.",
            "normal_fail": "A população não acreditou nas acusações contra seus aliados.",
            "low_critical": "Seus aliados apresentaram provas contra você e agravaram a crise."
        }
    ),
    Action(
        action_type="defense",
        alignment="bad",
        title="Coagir uma testemunha",
        description="Você tentará intimidar uma testemunha para impedir que ela revele informações comprometedoras.",
        risk_level="insane",
        responses={
            "high_critical": "A testemunha desistiu de prestar depoimento, mas o risco de investigação permanece.",
            "normal_success": "Não utilizado em ações insane.",
            "normal_fail": "Não utilizado em ações insane.",
            "low_critical": "A testemunha denunciou a intimidação e o caso se transformou em um grande escândalo."
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
        #Lógica de criar um objetos novamente porque eles ficar *detached* ao criados a primeira vez em uma mesma sessão
        #Ou seja, não mude.


if __name__ == "__main__":
    seed_actions()