from backend.app.models.db.action import Action
from sqlalchemy import delete

from backend.app.db.base import Base
from backend.app.db.database import SessionLocal, engine

ACTIONS = [
    Action(
        action_type="defense", alignment="corrupt", title="Negócio de Fachada",
        description="Você usa um comércio de fachada para lavar muito dinheiro vivo arrecadado da sua base.",
        risk_level="high",
        responses={"high_critical": "O dinheiro sujo é legalizado sem deixar rastros.", "normal_success": "Legaliza uma boa parte da grana acumulada.", "normal_fail": "A fiscalização financeira barra as transações da loja.", "low_critical": "O disfarce falha e o excesso de dinheiro expõe o esquema."}
    ),
    Action(
        action_type="defense", alignment="corrupt", title="Voos Oficiais para Férias",
        description="Você utiliza a frota do Estado para viagens de luxo particulares custeadas com dinheiro público.",
        risk_level="low",
        responses={"high_critical": "Desfruta de férias caras sem gastar do próprio bolso.", "normal_success": "Deslocamento concluído com mordomias pagas pelo erário (cofre público).", "normal_fail": "A imprensa fotografa seus gastos excessivos.", "low_critical": "O desvio de finalidade do voo vira um escândalo caro."}
    ),
    Action(
        action_type="defense", alignment="corrupt", title="Loteamento de Estatais",
        description="Em um acordo de bastidores, você distribui diretorias públicas para desviar dinheiro e comprar apoio.",
        risk_level="high",
        responses={"high_critical": "A base aliada garante blindagem total em troca de cargos lucrativos.", "normal_success": "Aliados mantêm sua estabilidade financeira e política.", "normal_fail": "A diretoria indicada gera rombos que vazam para a mídia.", "low_critical": "A polícia prende seus indicados com malas de dinheiro."}
    ),
    Action(
        action_type="defense", alignment="corrupt", title="Tráfico de Influência Familiar",
        description="Usando sua posição, você direciona contratos altamente lucrativos para empresas de parentes.",
        risk_level="medium",
        responses={"high_critical": "Sua família enriquece rapidamente com recursos públicos desviados.", "normal_success": "Negócios fechados garantem uma ótima comissão por fora.", "normal_fail": "Órgãos de controle abrem averiguação sobre o contrato.", "low_critical": "Áudios negociando a divisão do dinheiro vazam."}
    ),
    Action(
        action_type="defense", alignment="corrupt", title="Votação na Madrugada",
        description="Valendo-se de manobras protelatórias (atrasadoras), você aprova desvios orçamentários às escondidas na madrugada.",
        risk_level="low",
        responses={"high_critical": "A liberação de verbas passa sem contestação no plenário.", "normal_success": "O repasse de dinheiro é aprovado de forma silenciosa.", "normal_fail": "A oposição consegue quorum para barrar a votação.", "low_critical": "A sessão noturna vira um escândalo televisionado."}
    ),
    Action(
        action_type="defense", alignment="corrupt", title="Exoneração do Delegado",
        description="Para evitar investigações, você substitui o chefe policial que rastreava o caminho do seu dinheiro.",
        risk_level="high",
        responses={"high_critical": "A nova chefia engaveta os rastros financeiros.", "normal_success": "A investigação sobre o dinheiro some das prateleiras.", "normal_fail": "O delegado exonerado denuncia a interferência por propina.", "low_critical": "A justiça suspende a troca e aprofunda a quebra de sigilo."}
    ),
    Action(
        action_type="defense", alignment="corrupt", title="Orçamento Paralelo",
        description="Por meio de desvios, você repassa recursos do tesouro para fundações privadas controladas por laranjas.",
        risk_level="medium",
        responses={"high_critical": "Dinheiro público flui livremente para o seu caixa particular.", "normal_success": "Bula os trâmites e embolsa uma fatia generosa.", "normal_fail": "O Tribunal de Contas bloqueia as transferências suspeitas.", "low_critical": "As fundações fantasmas são esvaziadas pela polícia."}
    ),
    Action(
        action_type="defense", alignment="corrupt", title="Perdão Tributário a Aliados",
        description="Praticando favorecimento, você cancela dívidas fiscais de grandes empresas em troca de propina.",
        risk_level="medium",
        responses={"high_critical": "Empresas economizam muito dinheiro e enchem seu comitê de grana.", "normal_success": "O perdão passa disfarçado de incentivo com retorno financeiro.", "normal_fail": "Especialistas denunciam o acordo financeiro obscuro.", "low_critical": "O judiciário anula o perdão por corrupção explícita."}
    ),
    Action(
        action_type="defense", alignment="corrupt", title="Foro Privilegiado Instantâneo",
        description="Nomeia um aliado investigado para um cargo de alto escalão com o único objetivo de blindar seus bens.",
        risk_level="high",
        responses={"high_critical": "O processo sobe de instância e o dinheiro fica seguro.", "normal_success": "A apreensão dos bens do aliado é evitada.", "normal_fail": "Protestos populares contestam a nomeação blindada.", "low_critical": "A justiça anula a posse e decreta o confisco imediato."}
    ),
    Action(
        action_type="defense", alignment="corrupt", title="Rede de ONGs Fantasmas",
        description="Cria entidades sem fins lucrativos de mentira para embolsar repasses federais sem prestar serviços.",
        risk_level="medium",
        responses={"high_critical": "Fluxo constante de dinheiro público cai direto na sua conta.", "normal_success": "Repasses menores passam sem auditoria rigorosa.", "normal_fail": "Falta comprovação do uso do dinheiro recebido.", "low_critical": "A polícia encontra apenas um terreno baldio na sede da ONG."}
    ),
    Action(
        action_type="defense", alignment="corrupt", title="Inauguração de Obra Incompleta",
        description="Gasta dinheiro superfaturado em hospitais vazios apenas para lucrar na construção.",
        risk_level="low",
        responses={"high_critical": "Garante o desvio integral da verba e lucro máximo.", "normal_success": "A obra é dada como paga, gerando caixa por fora.", "normal_fail": "População percebe que o prédio está oco e sem equipamentos.", "low_critical": "A fachada mal paga desaba, revelando a roubalheira."}
    ),
    Action(
        action_type="defense", alignment="corrupt", title="Uso de Forças Paramilitares",
        description="Emprega milícias armadas para extorquir comerciantes locais e gerar renda paralela.",
        risk_level="high",
        responses={"high_critical": "Lucro imenso com a cobrança de taxas ilegais de proteção.", "normal_success": "Garante redutos financeiros blindados pela violência.", "normal_fail": "Os milicianos exigem fatias maiores do dinheiro arrecadado.", "low_critical": "O esquema de extorsão financeira é estourado pela polícia."}
    ),
    Action(
        action_type="defense", alignment="corrupt", title="Edital Viciado",
        description="Direciona licitações públicas para empresas que pagam as maiores comissões em dinheiro vivo.",
        risk_level="low",
        responses={"high_critical": "Empresa vencedora paga propina robusta em dinheiro vivo.", "normal_success": "O edital passa pelos fiscais mediante suborno leve.", "normal_fail": "Concorrentes denunciam o direcionamento do dinheiro público.", "low_critical": "O Ministério Público anula a licitação e prende o comitê."}
    ),
    Action(
        action_type="defense", alignment="corrupt", title="Destruição de Provas Contábeis",
        description="Destrói arquivos digitais e planilhas para apagar o histórico de propinas e desvios.",
        risk_level="high",
        responses={"high_critical": "Todos os rastros do dinheiro sujo somem para sempre.", "normal_success": "Garante anos de debate jurídico sobre as planilhas sumidas.", "normal_fail": "Cópias de segurança contábeis são recuperadas a tempo.", "low_critical": "Peritos recuperam os arquivos provando o roubo."}
    ),
    Action(
        action_type="defense", alignment="corrupt", title="Escudo Ideológico",
        description="Usa discursos morais vazios para abafar denúncias de que você embolsou verbas públicas.",
        risk_level="low",
        responses={"high_critical": "Sua base fanatizada ignora os desvios de dinheiro.", "normal_success": "Desgasta a credibilidade de quem investiga suas contas.", "normal_fail": "Instituições sérias expõem seus extratos bancários.", "low_critical": "Você é flagrado ostentando itens de luxo incompatíveis."}
    ),
    Action(
        action_type="defense", alignment="corrupt", title="Viagem Estratégica de Ausência",
        description="Foge para o exterior com dinheiro na mala no dia em que seria intimado pela justiça.",
        risk_level="low",
        responses={"high_critical": "Aproveita sua fortuna intocável hospedado em hotéis de luxo.", "normal_success": "A intimação é adiada enquanto você gasta sua grana fora.", "normal_fail": "A justiça emite alerta de confisco de bens internacionais.", "low_critical": "Seus gastos milionários no exterior vazam na imprensa."}
    ),
    Action(
        action_type="defense", alignment="corrupt", title="Chantagem Orçamentária",
        description="Retém dinheiro de prefeituras rivais até que aceitem pagar propina política.",
        risk_level="medium",
        responses={"high_critical": "Prefeitos rivais cedem e liberam verbas paralelas para você.", "normal_success": "Garante fluxo financeiro em troca de emendas.", "normal_fail": "Prefeitos denunciam a extorsão financeira em público.", "low_critical": "O escândalo de achaque de verbas vira CPI."}
    ),
    Action(
        action_type="defense", alignment="corrupt", title="Terceirização da Culpa",
        description="Suborna subordinados para assumirem a responsabilidade exclusiva pelo dinheiro desviado.",
        risk_level="low",
        responses={"high_critical": "Você sai ileso enquanto o laranja assume a culpa e a cadeia.", "normal_success": "Cria uma cortina de fumaça e mantém seu dinheiro seguro.", "normal_fail": "Documentos oficiais apontam que a ordem do roubo foi sua.", "low_critical": "O laranja assume a culpa, mas faz delação cobrando mais dinheiro."}
    ),
    Action(
        action_type="defense", alignment="corrupt", title="Caixa Oculto em Espécie",
        description="Guarda malas cheias de dinheiro vivo em cofres e apartamentos de fachada.",
        risk_level="medium",
        responses={"high_critical": "Mantém fortunas invisíveis prontas para uso imediato.", "normal_success": "Garante suprimento de grana livre de banco.", "normal_fail": "Transportadores de dinheiro são pegos em blitzes.", "low_critical": "A polícia estoura o apartamento e filma as montanhas de dinheiro."}
    ),
    Action(
        action_type="defense", alignment="corrupt", title="Plantão Judiciário Noturno",
        description="Suborna magistrados de plantão na calada da noite para liberarem contas e bens bloqueados.",
        risk_level="high",
        responses={"high_critical": "Seu dinheiro bloqueado é liberado na calada da noite.", "normal_success": "Neutraliza o confisco de recursos ilícitos.", "normal_fail": "O plenário do tribunal cassa a liminar corrupta no dia útil seguinte.", "low_critical": "O juiz plantonista é pego com maços de dinheiro em casa."}
    ),
    Action(
        action_type="defense", alignment="corrupt", title="Desvio de Obras de Infraestrutura",
        description="Superfatura custos de construções públicas para dividir o lucro excedente com empreiteiras.",
        risk_level="high",
        responses={"high_critical": "Suga fortunas das obras públicas direto para o seu bolso.", "normal_success": "Constrói o essencial e embolsa o resto do dinheiro.", "normal_fail": "A estrutura apresenta falhas graves por economia de material.", "low_critical": "A construtora quebra e deixa o dinheiro da obra sumido."}
    ),
    Action(
        action_type="defense", alignment="corrupt", title="Conta Secreta em Jurisdição Externa",
        description="Abre contas em paraísos fiscais no exterior para guardar dinheiro de suborno.",
        risk_level="medium",
        responses={"high_critical": "Patrimônio milionário totalmente blindado em dólar.", "normal_success": "Garante reservas intocáveis no exterior.", "normal_fail": "Vazamentos de bancos estrangeiros expõem suas contas.", "low_critical": "Tribunais internacionais congelam seu dinheiro por ilicitude."}
    ),
    Action(
        action_type="defense", alignment="corrupt", title="Desvio de Salários de Assessores",
        description="Exige a devolução de parte dos salários de funcionários do gabinete em benefício próprio.",
        risk_level="medium",
        responses={"high_critical": "Enriquece mensalmente à custa do salário alheio.", "normal_success": "Garante uma mesada extra livre de impostos.", "normal_fail": "Assalariados guardam comprovantes de saque do dinheiro.", "low_critical": "Ex-funcionário expõe o recolhimento de dinheiro na TV."}
    ),
    Action(
        action_type="defense", alignment="corrupt", title="Uso Privativo de Cartão de Estado",
        description="Paga despesas pessoais extravagantes utilizando cartões corporativos públicos.",
        risk_level="low",
        responses={"high_critical": "Mantém padrão de vida milionário sem tocar no próprio dinheiro.", "normal_success": "Festas e hotéis de luxo pagos com dinheiro público.", "normal_fail": "Auditoria expõe notas fiscais de gastos absurdos.", "low_critical": "O escândalo obriga a devolução de todo o dinheiro gasto."}
    ),
    Action(
        action_type="defense", alignment="corrupt", title="Ocultação de Imóveis Rurais",
        description="Compra fazendas luxuosas utilizando testas de ferro (laranjas) para esconder seu patrimônio.",
        risk_level="medium",
        responses={"high_critical": "Territórios valiosos intocáveis por investigações de enriquecimento.", "normal_success": "Oculta a origem do dinheiro usado nas compras.", "normal_fail": "Parentes dos laranjas entram em disputa judicial pelas terras.", "low_critical": "O laranja confessa que você é o verdadeiro dono das fazendas."}
    ),
    Action(
        action_type="defense", alignment="corrupt", title="Substituição de Insumos Básicos",
        description="Economiza dinheiro comprando materiais de péssima qualidade para o Estado e embolsa a sobra.",
        risk_level="high",
        responses={"high_critical": "Maximiza o lucro ilícito com a diferença do dinheiro economizado.", "normal_success": "Entrega serviços baratos e embolsa a sobra do orçamento.", "normal_fail": "Usuários denunciam a precariedade dos produtos entregues.", "low_critical": "Fiscalização condena o lote e exige devolução do dinheiro."}
    ),
    Action(
        action_type="defense", alignment="corrupt", title="Proteção a Cartéis de Transporte",
        description="Recebe propina mensal de empresas de ônibus para evitar multas por falhas no serviço.",
        risk_level="high",
        responses={"high_critical": "Caixa dois recheado todo mês com dinheiro das passagens.", "normal_success": "Mantém o setor submisso em troca de vista grossa.", "normal_fail": "População revolta-se e incendeia ônibus contra a tarifa.", "low_critical": "Diretores do cartel fazem delação sobre a propina paga."}
    ),
    Action(
        action_type="defense", alignment="corrupt", title="Afroxamento de Licenciamento Ambiental",
        description="Libera desmatamentos ilegais em troca de participação financeira nos lucros da terra.",
        risk_level="high",
        responses={"high_critical": "Grandes madeireiras enchem seu bolso de dinheiro.", "normal_success": "Acelera licenças mediante pagamento de taxas por fora.", "normal_fail": "Imagens de satélite alertam órgãos de controle internacional.", "low_critical": "O esquema de propina ambiental é exposto em rede nacional."}
    ),
    Action(
        action_type="defense", alignment="corrupt", title="Regularização de Grilagem",
        description="Vende títulos de terras públicas invadidas para especuladores imobiliários.",
        risk_level="medium",
        responses={"high_critical": "Lucra fortunas vendendo o que pertence ao Estado.", "normal_success": "Consolida lucros rápidos com terras griladas.", "normal_fail": "Movimentos sociais barram a venda na justiça.", "low_critical": "Confrontos de terra revelam a venda ilegal de lotes."}
    ),
    Action(
        action_type="defense", alignment="corrupt", title="Compra de Decisões de Instância",
        description="Paga propina em dinheiro vivo a intermediários do judiciário em troca de sentenças favoráveis.",
        risk_level="high",
        responses={"high_critical": "Elimina qualquer barreira legal contra seus negócios ilícitos.", "normal_success": "Garante decisões vantajosas mediante pagamento.", "normal_fail": "O tribunal superior anula a sentença comprada.", "low_critical": "A Polícia Federal prende o intermediário com maletas de dinheiro."}
    ),
    Action(
        action_type="defense", alignment="corrupt", title="Anistia a Multas de Grandes Poluidores",
        description="Perdoa multas ambientais pesadas em troca de doações financeiras ocultas para sua campanha.",
        risk_level="medium",
        responses={"high_critical": "Empresas poluidoras financiam sua vida de luxo.", "normal_success": "Abate multas pendentes mediante acordos financeiros por fora.", "normal_fail": "Ministério Público anula os perdões e investiga as contas.", "low_critical": "Desastres ambientais tornam o perdão de multas indefensável."}
    ),
    Action(
        action_type="defense", alignment="corrupt", title="Acúmulo Indevido de Benefícios",
        description="Cria brechas e inventa auxílios absurdos para inchar o próprio salário mensal.",
        risk_level="low",
        responses={"high_critical": "Eleva seus rendimentos mensais com dinheiro público.", "normal_success": "Garante supersalários sem trabalhar a mais.", "normal_fail": "Imprensa expõe a farra dos auxílios em manchetes.", "low_critical": "Pressão pública obriga o corte e devolução do dinheiro."}
    ),
    Action(
        action_type="defense", alignment="corrupt", title="Emendas Discricionárias Ocultas",
        description="Repassa dinheiro do orçamento para prefeituras aliadas em troca de devolução em espécie.",
        risk_level="high",
        responses={"high_critical": "Prefeitos devolvem uma porcentagem do dinheiro em espécie.", "normal_success": "Alimenta redutos eleitorais com verbas direcionadas.", "normal_fail": "Falta de prestação de contas bloqueia o dinheiro.", "low_critical": "Tribunal aponta desvio e propina nas emendas."}
    ),
    Action(
        action_type="defense", alignment="corrupt", title="Cartéis de Obras Públicas",
        description="Divide licitações de obras entre empreiteiras que pagam propina garantida.",
        risk_level="medium",
        responses={"high_critical": "Construtoras mantêm seu cofre particular sempre abastecido.", "normal_success": "Obras executadas com superfaturamento garantido.", "normal_fail": "Empresa de fora denuncia o esquema de propina.", "low_critical": "Delação de executivo expõe a divisão do dinheiro sujo."}
    ),
    Action(
        action_type="defense", alignment="corrupt", title="Emissão de Notas Frias",
        description="Emite notas de serviços fantasmas para justificar o dinheiro desviado do governo.",
        risk_level="low",
        responses={"high_critical": "Balanço fechado sem sobras suspeitas de dinheiro.", "normal_success": "Despesas falsas justificam o dinheiro em caixa.", "normal_fail": "Fiscais descobrem que a empresa emissora não existe.", "low_critical": "Dono da empresa fantasma confessa a lavagem de dinheiro."}
    ),
    Action(
        action_type="defense", alignment="corrupt", title="Concessão de Imunidade Aduaneira",
        description="Facilita o contrabando de mercadorias em troca de propina nas fronteiras.",
        risk_level="low",
        responses={"high_critical": "Carga ilegal passa livre gerando muito dinheiro por fora.", "normal_success": "Agiliza o contrabando de parceiros pagantes.", "normal_fail": "Alfândega intercepta o contrabando por denúncia.", "low_critical": "Apreensão de mercadorias expõe a propina na alfândega."}
    ),
    Action(
        action_type="defense", alignment="corrupt", title="Rodízio de Cargos Familiares",
        description="Revezar parentes em secretarias para continuar movimentando dinheiro público sem controle.",
        risk_level="medium",
        responses={"high_critical": "Mantém o clã familiar controlando o fluxo de dinheiro do Estado.", "normal_success": "Preserva o acesso direto às contas públicas.", "normal_fail": "Ministério Público enquadra a manobra como fraude financeira.", "low_critical": "Protestos exigem fim do esquema familiar de desvio."}
    ),
    Action(
        action_type="defense", alignment="corrupt", title="Extorsão de Licenciamentos",
        description="Fiscais travam negócios até que proprietários paguem propina em dinheiro vivo.",
        risk_level="medium",
        responses={"high_critical": "Mantém fluxo constante de dinheiro vivo entrando no gabinete.", "normal_success": "Comércio local submete-se ao pagamento exigido.", "normal_fail": "Empresário grava a cobrança de propina e aciona a polícia.", "low_critical": "Rebelião de comerciantes paralisa a secretaria de fiscais."}
    ),
    Action(
        action_type="defense", alignment="corrupt", title="Decretos de Urgência Falsos",
        description="Simula emergências climáticas ou sanitárias para dispensar licitações e desviar dinheiro direto.",
        risk_level="high",
        responses={"high_critical": "Contrata empresas de fachada e fatura com o superfaturamento.", "normal_success": "Dinheiro público liberado sem burocracia.", "normal_fail": "Órgãos de controle provam que não havia emergência nenhuma.", "low_critical": "O desvio de dinheiro em situação normal é descoberto."}
    ),
    Action(
        action_type="defense", alignment="corrupt", title="Publicidade Institucional Chapa-Branca",
        description="Usa verba de comunicação estatal para enriquecer agências amigas que devolvem caixa dois.",
        risk_level="low",
        responses={"high_critical": "Desvia fortunas da publicidade para seu caixa de campanha.", "normal_success": "Abafa críticas pagando jornais com dinheiro público.", "normal_fail": "Mídia independente expõe os contratos superfaturados.", "low_critical": "Agência de publicidade devolve dinheiro e delata o esquema."}
    ),
    Action(
        action_type="defense", alignment="corrupt", title="Sigilo de Encontros Oficiais",
        description="Esconde reuniões com lobistas para acobertar negociações de propina milionária.",
        risk_level="medium",
        responses={"high_critical": "Acordos escusos e transferência de dinheiro livres de exames.", "normal_success": "Evita questionamentos sobre quem financia sua gestão.", "normal_fail": "O judiciário obriga a publicação dos registros de visitas.", "low_critical": "Documentos vazados revelam malas de dinheiro combinadas."}
    ),
    Action(
        action_type="defense", alignment="corrupt", title="Recepção de Presentes de Alto Valor",
        description="Aceita joias e relógios caríssimos de presente em troca de favores políticos acobertados.",
        risk_level="high",
        responses={"high_critical": "Acumula bens de luxo valiosos escondidos no cofre.", "normal_success": "Presentes caros guardados sem registro patrimonial.", "normal_fail": "Receita Federal apreende os itens caros na alfândega.", "low_critical": "A origem duvidosa dos presentes caros vira escândalo."}
    ),
    Action(
        action_type="defense", alignment="good", title="Digitalização de Serviços",
        description="Moderniza a burocracia estatal em plataformas digitais ágeis e acessíveis.",
        risk_level="low",
        responses={"high_critical": "Gera economia expressiva e agilidade operacional exemplar.", "normal_success": "Reduz drasticamente as filas em órgãos públicos.", "normal_fail": "Sistemas enfrentam instabilidade inicial.", "low_critical": "Falha de segurança expõe dados cadastrais."}
    ),
    Action(
        action_type="defense", alignment="good", title="Concessão Rodoviária Rigorosa",
        description="Delega rodovias à iniciativa privada com metas estritas e fiscalizadas de manutenção.",
        risk_level="medium",
        responses={"high_critical": "Malha viária impecável impulsiona a economia regional.", "normal_success": "Elimina gastos estatais com reparos básicos.", "normal_fail": "Motoristas protestam contra valores de pedágio.", "low_critical": "A concessionária falha e abandona os trechos."}
    ),
    Action(
        action_type="defense", alignment="good", title="Escola de Tempo Integral",
        description="Amplia a jornada escolar com atividades culturais, esporte e refeições de qualidade.",
        risk_level="medium",
        responses={"high_critical": "Reduz a vulnerabilidade juvenil e eleva índices educacionais.", "normal_success": "Oferece rede de apoio essencial para famílias trabalhadoras.", "normal_fail": "Infraestrutura escolar carece de adaptações.", "low_critical": "Falta de repasses interrompe o programa."}
    ),
    Action(
        action_type="defense", alignment="good", title="Fundo Soberano Regional",
        description="Poupa excedentes de arrecadação em investimentos de longo prazo para garantir segurança financeira.",
        risk_level="high",
        responses={"high_critical": "Protege o estado contra flutuações e crises severas.", "normal_success": "Consolida crédito sólido perante o mercado.", "normal_fail": "Oposição tenta desviar reservas para gastos correntes.", "low_critical": "Crise financeira global corrói parte do fundo."}
    ),
    Action(
        action_type="defense", alignment="good", title="Reforma Tributária Simplificada",
        description="Elimina impostos em cascata e desburocratiza a abertura de novos negócios.",
        risk_level="medium",
        responses={"high_critical": "Multiplica o surgimento de novas empresas e empregos.", "normal_success": "Facilita a regularização de pequenos empreendedores.", "normal_fail": "Prefeituras resistem à perda de arrecadação local.", "low_critical": "Erros na transição geram insegurança fiscal temporária."}
    ),
    Action(
        action_type="defense", alignment="good", title="Segurança Hídrica Estrutural",
        description="Instala cisternas e adutoras para assegurar o abastecimento de água no semiárido.",
        risk_level="low",
        responses={"high_critical": "Elimina a vulnerabilidade à seca e estimula produção rural.", "normal_success": "Garante água potável em comunidades isoladas.", "normal_fail": "Licenciamentos ambientais atrasam o cronograma.", "low_critical": "Problemas técnicos danificam tubulações."}
    ),
    Action(
        action_type="defense", alignment="good", title="Fronteiras Tecnológicas",
        description="Emprega sistemas de monitoramento eletrônico para coibir o crime transfronteiriço.",
        risk_level="medium",
        responses={"high_critical": "Asfixia rotas de contrabando sem conflitos armados urbanos.", "normal_success": "Aumenta a segurança com eficiência técnica.", "normal_fail": "Grupos criminosos adaptam rotas alternativas.", "low_critical": "Ataque cibernético compromete os sensores de fronteira."}
    ),
    Action(
        action_type="defense", alignment="good", title="Diplomacia Verde",
        description="Atrai cooperação internacional estritamente vinculada à preservação ambiental.",
        risk_level="low",
        responses={"high_critical": "Injeta recursos externos na economia de preservação local.", "normal_success": "Garante reconhecimento e apoio em fóruns globais.", "normal_fail": "Setores produtivos tradicionais criticam os acordos.", "low_critical": "Infrações ambientais cancelam os aportes externos."}
    ),
    Action(
        action_type="defense", alignment="good", title="Conectividade Rural Avançada",
        description="Leva banda larga a escolas e postos de saúde em regiões remotas e isoladas.",
        risk_level="medium",
        responses={"high_critical": "Integra comunidades distantes à rede econômica e educacional.", "normal_success": "Garante acesso a serviços digitais básicos.", "normal_fail": "Custos de manutenção de antenas superam o previsto.", "low_critical": "Equipamentos são vandalizados após a instalação."}
    ),
    Action(
        action_type="defense", alignment="good", title="Polo de Inovação Tecnológica",
        description="Estimula parcerias diretas entre centros de pesquisa e indústrias locais.",
        risk_level="medium",
        responses={"high_critical": "Gera patentes de alto valor e retém talentos na região.", "normal_success": "Fomenta o surgimento de startups inovadoras.", "normal_fail": "Falta adesão do setor industrial tradicional.", "low_critical": "Parceiros privados abandonam o projeto."}
    ),
    Action(
        action_type="defense", alignment="good", title="Regularização Fundiária Cidadã",
        description="Concede títulos de propriedade definitivos garantindo segurança jurídica aos moradores.",
        risk_level="low",
        responses={"high_critical": "Garante segurança jurídica e acesso a crédito popular.", "normal_success": "Promove inclusão e cidadania nas comunidades.", "normal_fail": "Cartórios registram lentidão na emissão de papéis.", "low_critical": "Especuladores expulsam beneficiários recém-titulados."}
    ),
    Action(
        action_type="defense", alignment="good", title="Política de Valorização de Renda",
        description="Ajusta o poder de compra da base popular para dinamizar o mercado interno.",
        risk_level="high",
        responses={"high_critical": "Aquecer o comércio local gera ciclo virtuoso de consumo.", "normal_success": "Reduz indicadores de desigualdade social imediata.", "normal_fail": "Pressões inflacionárias corroem parte do ganho.", "low_critical": "Pequenos comerciantes sofrem com custos trabalhistas."}
    ),
    Action(
        action_type="defense", alignment="good", title="Expansão Ferroviária",
        description="Implementa malha de trens de carga para baratear o frete regional de forma sustentável.",
        risk_level="high",
        responses={"high_critical": "Revoluciona a logística e reduz custos de mercadorias.", "normal_success": "Desafoga o tráfego pesado nas rodovias estaduais.", "normal_fail": "Burocracia de desapropriação atrasa trilhos.", "low_critical": "Erros de planejamento obrigam paralisação das obras."}
    ),
    Action(
        action_type="defense", alignment="good", title="Limite de Gastos com Altas Cúpulas",
        description="Estabelece tetos rígidos para privilégios no alto funcionalismo público.",
        risk_level="high",
        responses={"high_critical": "Equilibra as contas públicas e exemplifica austeridade.", "normal_success": "Libera verbas para investimentos em áreas sociais.", "normal_fail": "Setores jurídicos respondem com paralisações.", "low_critical": "Tribunais revertem o corte por vício de competência."}
    ),
    Action(
        action_type="defense", alignment="good", title="Habitação Sustentável Integrada",
        description="Constrói conjuntos habitacionais equipados com energia solar e saneamento básico.",
        risk_level="medium",
        responses={"high_critical": "Garante moradia digna e reduz custos fixos das famílias.", "normal_success": "Diminui o déficit habitacional da região.", "normal_fail": "Atrasos na entrega frustram famílias cadastradas.", "low_critical": "Falhas estruturais exigem reformas corretivas."}
    ),
    Action(
        action_type="defense", alignment="good", title="Eventos Globais de Sustentabilidade",
        description="Sedia conferências internacionais de grande porte pautadas na responsabilidade climática.",
        risk_level="low",
        responses={"high_critical": "Atrai investimentos turísticos e projeta o estado globalmente.", "normal_success": "Fortalece a imagem de gestão moderna.", "normal_fail": "Protestos bloqueiam vias de acesso ao evento.", "low_critical": "Falhas de infraestrutura urbana expõem a gestão."}
    ),
    Action(
        action_type="defense", alignment="good", title="Aprovação Automática Comercial",
        description="Simplifica licenças por meio de desburocratização para empreendimentos de baixo risco.",
        risk_level="low",
        responses={"high_critical": "Multiplica a abertura de comércios e reduz burocracia.", "normal_success": "Agiliza a formalização de trabalhadores autônomos.", "normal_fail": "Fiscais tradicionais tentam burlar o sistema online.", "low_critical": "Atividades perigosas obtêm alvará por falha sistêmica."}
    ),
    Action(
        action_type="defense", alignment="good", title="Mutirão de Atendimento Médico",
        description="Organiza forças-tarefas com rigor técnico para zerar filas de exames especializados.",
        risk_level="medium",
        responses={"high_critical": "Resolve gargalos históricos e alivia o sistema de saúde.", "normal_success": "Atende centenas de pacientes reprimidos.", "normal_fail": "Profissionais de saúde esgotam-se com a jornada extra.", "low_critical": "Falta de insumos básicos paralisa os mutirões."}
    ),
    Action(
        action_type="defense", alignment="good", title="Crédito Bancário Acessível",
        description="Fomenta linhas de financiamento com juros baixos voltadas a pequenos empreendedores.",
        risk_level="high",
        responses={"high_critical": "Estimula o ecossistema empreendedor local com segurança.", "normal_success": "Oferece fôlego a pequenos produtores.", "normal_fail": "Bancos privados impõem barreiras concorrenciais.", "low_critical": "Índice elevado de inadimplência descapitaliza o fundo."}
    ),
    Action(
        action_type="defense", alignment="good", title="Passe Livre Estudantil",
        description="Garante gratuidade no transporte público para estudantes da rede pública de ensino.",
        risk_level="medium",
        responses={"high_critical": "Garante acesso universal à escola e reduz evasão.", "normal_success": "Alivia o orçamento de famílias de baixa renda.", "normal_fail": "Empresas operadoras exigem repasses maiores.", "low_critical": "Fraudes em cadastros exigem recadastramento geral."}
    ),
    Action(
        action_type="defense", alignment="good", title="Transição Energética Municipal",
        description="Instala painéis solares em prédios e escolas públicas para matriz limpa.",
        risk_level="medium",
        responses={"high_critical": "Gera economia expressiva em contas de luz institucionais.", "normal_success": "Promove matriz energética limpa na prática.", "normal_fail": "Manutenção dos painéis apresenta atrasos.", "low_critical": "Fornecedores entregam equipamentos defeituosos."}
    ),
    Action(
        action_type="defense", alignment="good", title="Microcrédito Social Orientado",
        description="Concede pequenos empréstimos atrelados a capacitação para microempreendedoras.",
        risk_level="medium",
        responses={"high_critical": "Fomenta a economia popular e gera independência financeira.", "normal_success": "Movimenta o comércio nos bairros periféricos.", "normal_fail": "Dificuldade de acompanhamento técnico em alguns locais.", "low_critical": "Uso político do programa desvia o foco original."}
    ),
    Action(
        action_type="defense", alignment="good", title="Monitoramento Policial Transparente",
        description="Implementa registros audiovisuais em operações para garantir lisura policial.",
        risk_level="high",
        responses={"high_critical": "Reduz conflitos letais e eleva a confiança institucional.", "normal_success": "Protege os próprios agentes contra falsas acusações.", "normal_fail": "Resistência interna de setores corporativos da tropa.", "low_critical": "Falhas técnicas em equipamentos comprometem registros."}
    ),
    Action(
        action_type="defense", alignment="good", title="Preservação de Mananciais Urbanos",
        description="Cria parques de proteção em áreas de nascentes para salvaguardar o abastecimento.",
        risk_level="low",
        responses={"high_critical": "Assegura qualidade hídrica a longo prazo para a população.", "normal_success": "Recupera áreas verdes degradadas na cidade.", "normal_fail": "Remoção de ocupações irregulares gera conflitos.", "low_critical": "Novas invasões destroem a vegetação protegida."}
    ),
    Action(
        action_type="defense", alignment="good", title="Parques Lineares Urbanos",
        description="Converte margens de rios abandonadas em áreas verdes de lazer e esporte coletivo.",
        risk_level="low",
        responses={"high_critical": "Revitaliza regiões degradadas e melhora o bem-estar coletivo.", "normal_success": "Cria espaços públicos de convivência de qualidade.", "normal_fail": "Falta de manutenção pública degrada os equipamentos.", "low_critical": "Áreas de lazer tornam-se pontos de criminalidade noturna."}
    ),
    Action(
        action_type="defense", alignment="good", title="Auditoria Independente de Contas",
        description="Submete o orçamento estadual a análises acadêmicas públicas e imparciais.",
        risk_level="high",
        responses={"high_critical": "Identifica desperdícios e otimiza alocação de recursos.", "normal_success": "Consolida a reputação de probidade (honestidade) administrativa.", "normal_fail": "Relatórios técnicos geram debates burocráticos infindáveis.", "low_critical": "Auditoria aponta falhas graves na própria gestão atual."}
    ),
    Action(
        action_type="defense", alignment="good", title="Portal de Dados Abertos",
        description="Disponibiliza cada centavo executado pelo governo em tempo real na internet.",
        risk_level="low",
        responses={"high_critical": "Garante máxima transparência e controle social ativo.", "normal_success": "Facilita o trabalho de fiscalização da imprensa e cidadãos.", "normal_fail": "Plataforma sofre instabilidades de acesso.", "low_critical": "Erros de lançamento de dados geram confusão pública."}
    ),
    Action(
        action_type="defense", alignment="good", title="Merenda Orgânica Local",
        description="Direciona compras da alimentação escolar para pequenos agricultores familiares.",
        risk_level="medium",
        responses={"high_critical": "Nutrição de qualidade e fortalecimento da economia rural.", "normal_success": "Incentiva produção sustentável na região.", "normal_fail": "Cooperativas locais enfrentam gargalos logísticos.", "low_critical": "Desvios em entregas prejudicam o cardápio escolar."}
    ),
    Action(
        action_type="defense", alignment="good", title="Cinturões Verdes Municipais",
        description="Estabelece zonas de restrição agrícola sustentável ao redor de centros urbanos.",
        risk_level="medium",
        responses={"high_critical": "Garante produção de alimentos limpos próximos aos centros.", "normal_success": "Controla a expansão urbana desordenada.", "normal_fail": "Pressão imobiliária contesta os limites das zonas.", "low_critical": "Abandono das áreas fomenta ocupações irregulares."}
    ),
    Action(
        action_type="defense", alignment="good", title="Incentivo a Editais Culturais Descentralizados",
        description="Fomenta produções artísticas locais em periferias através de critérios meritocráticos.",
        risk_level="low",
        responses={"high_critical": "Estimula a economia criativa e engaja novos públicos.", "normal_success": "Valoriza expressões culturais regionais diversas.", "normal_fail": "Critérios de seleção geram contestação burocrática.", "low_critical": "Recursos são direcionados a projetos sem relevância."}
    ),
    Action(
        action_type="defense", alignment="good", title="Ações Afirmativas Meritocráticas",
        description="Garante suporte estrutural em programas públicos de capacitação inclusiva.",
        risk_level="medium",
        responses={"high_critical": "Corrige assimetrias históricas no acesso a oportunidades.", "normal_success": "Promove diversidade nos quadros profissionais.", "normal_fail": "Contestações jurídicas atrasam o cronograma.", "low_critical": "Fraudes em comprovações exigem revisão rigorosa."}
    ),
    Action(
        action_type="defense", alignment="good", title="Cooperativas de Reciclagem Oficial",
        description="Integra catadores à rede oficial de saneamento e limpeza urbana com direitos.",
        risk_level="low",
        responses={"high_critical": "Profissionaliza o setor e reduz o volume de lixo descartado.", "normal_success": "Melhora indicadores de limpeza e sustentabilidade.", "normal_fail": "Resistência de empresas tradicionais de coleta.", "low_critical": "Incêndios criminosos destroem centrais de reciclagem."}
    ),
    Action(
        action_type="defense", alignment="good", title="Creches de Horário Ampliado",
        description="Oferece atendimento infantil noturno para apoiar pais que estudam e trabalham.",
        risk_level="high",
        responses={"high_critical": "Garante amparo educacional e possibilita inserção laboral.", "normal_success": "Amplia a rede de apoio às famílias vulneráveis.", "normal_fail": "Dificuldade em compor equipes para turnos estendidos.", "low_critical": "Acidentes na unidade expõem falhas de supervisão."}
    ),
    Action(
        action_type="defense", alignment="good", title="Capacitação Antifraude Digital",
        description="Educa comunidades vulneráveis sobre salvaguardas contra golpes virtuais.",
        risk_level="low",
        responses={"high_critical": "Reduz drasticamente incidência de fraudes contra idosos.", "normal_success": "Promove letramento digital prático.", "normal_fail": "Baixo engajamento em algumas faixas etárias.", "low_critical": "Golpistas adaptam métodos e burlam as orientações."}
    ),
    Action(
        action_type="defense", alignment="good", title="Descentralização de Postos de Vacinação",
        description="Leva imunização a locais de grande circulação para ampliar o alcance público.",
        risk_level="low",
        responses={"high_critical": "Eleva coberturas vacinais prevenindo surtos regionais.", "normal_success": "Facilita o acesso da população trabalhadora.", "normal_fail": "Grupos antivacina promovem protestos locais.", "low_critical": "Falhas na cadeia de frio perdem lotes de vacinas."}
    ),
    Action(
        action_type="defense", alignment="good", title="Plano Preventivo de Defesa Civil",
        description="Mapeia riscos e executa obras de contenção antes do período sazonal de chuvas.",
        risk_level="medium",
        responses={"high_critical": "Evita tragédias e protege vidas em áreas vulneráveis.", "normal_success": "Minimiza impactos de temporais recorrentes.", "normal_fail": "Ocupações continuam em zonas de risco interditadas.", "low_critical": "Obras pontuais cedem com volumes atípicos de chuva."}
    ),
    Action(
        action_type="defense", alignment="good", title="Seguro Social Regional de Amparo",
        description="Institui rede de proteção temporária para trabalhadores autônomos em recessão.",
        risk_level="high",
        responses={"high_critical": "Evita colapso econômico familiar em momentos de crise.", "normal_success": "Ampara setores informais da economia.", "normal_fail": "Custo orçamentário inicial pressiona o fisco.", "low_critical": "Fraudes cadastrais exigem suspensão do benefício."}
    ),
    Action(
        action_type="defense", alignment="good", title="Urbanização Integrada de Assentamentos",
        description="Leva saneamento e infraestrutura básica a comunidades periféricas consolidadas.",
        risk_level="high",
        responses={"high_critical": "Integra a periferia à cidade formal com dignidade.", "normal_success": "Melhora indicadores sanitários locais.", "normal_fail": "Complexidade topográfica atrasa o cronograma.", "low_critical": "Falta de manutenção posterior degrada as melhorias."}
    ),
    Action(
        action_type="defense", alignment="good", title="Revitalização de Centros Históricos",
        description="Incentiva habitação e comércios populares em zonas centrais degradadas.",
        risk_level="medium",
        responses={"high_critical": "Resgata o valor cultural e econômico de áreas abandonadas.", "normal_success": "Atrai novos moradores para o coração da cidade.", "normal_fail": "Custos de restauro afetam investidores menores.", "low_critical": "Processo de gentrificação expulsa moradores antigos."}
    ),
    Action(
        action_type="defense", alignment="good", title="Reforma Agrária Consolidada",
        description="Assenta famílias em terras improdutivas com suporte técnico rigoroso.",
        risk_level="medium",
        responses={"high_critical": "Garante produção de alimentos e paz social no campo.", "normal_success": "Fixa trabalhadores no campo com autonomia.", "normal_fail": "Conflitos com proprietários atrasam titulações.", "low_critical": "Falta de escoamento prejudica a produção dos assentados."}
    ),
    Action(
        action_type="defense", alignment="good", title="Transporte Fluvial Sustentável",
        description="Utiliza vias navegáveis urbanas para linhas eficientes e limpas de passageiros.",
        risk_level="high",
        responses={"high_critical": "Alivia o trânsito rodoviário com transporte limpo.", "normal_success": "Oferece alternativa agradável de deslocamento.", "normal_fail": "Oscilações no nível dos rios atrapalham a operação.", "low_critical": "Embarcações colidem com detritos acumulados."}
    ),
    Action(
        action_type="defense", alignment="good", title="Hospitais Modulares Rápidos",
        description="Instala unidades hospitalares de alta tecnologia em prazos recordes validados.",
        risk_level="medium",
        responses={"high_critical": "Amplia a capacidade de atendimento em momentos críticos.", "normal_success": "Garante suporte rápido a regiões desassistidas.", "normal_fail": "Custos operacionais elevados a longo prazo.", "low_critical": "Materiais de construção apresentam desgaste prematuro."}
    ),
     Action(
        action_type="attack", alignment="corrupt", title="Dossiê Anônimo",
        description="Paga tabloides para propagar inverdades que desestabilizam o rival político.",
        risk_level="low",
        responses={"high_critical": "Manchetes compradas travam a campanha do rival.", "normal_success": "Força o adversário a gastar muito dinheiro se defendendo.", "normal_fail": "Veículos rejeitam a pauta por falta de provas.", "low_critical": "Descobrem que você pagou pela farsa com dinheiro desviado."}
    ),
    Action(
        action_type="attack", alignment="corrupt", title="Rotulação Ideológica Extrema",
        description="Financia propaganda suja para colar rótulos falsos e gerar aversão ao oponente.",
        risk_level="low",
        responses={"high_critical": "Eleitores abandonam o rival apavorados com o boato.", "normal_success": "Cria rejeição alta usando propaganda paga.", "normal_fail": "O eleitorado percebe que foi uma campanha cara e falsa.", "low_critical": "A tática custa caro e o dinheiro investido dá prejuízo político."}
    ),
    Action(
        action_type="attack", alignment="corrupt", title="Paralisação Policial Oculta",
        description="Por meio de suborno por fora, instiga protestos artificiais na segurança pública rival.",
        risk_level="high",
        responses={"high_critical": "A insegurança gerada paralisa a administração oponente.", "normal_success": "Gera desgaste político imediato ao governo rival.", "normal_fail": "A cúpula policial neutraliza a agitação paga.", "low_critical": "O pagamento de propina aos grevistas é descoberto."}
    ),
    Action(
        action_type="attack", alignment="corrupt", title="Manipulação Sintética de Mídia",
        description="Contrata serviços escusos para fabricar áudios falsos incriminando o oponente.",
        risk_level="high",
        responses={"high_critical": "O material falso comprado corrói a base do oponente.", "normal_success": "Semeia dúvidas duradouras usando mídia cara.", "normal_fail": "Peritos de alto nível desmantelam a falsificação.", "low_critical": "A fatura do serviço hacker é encontrada em suas contas."}
    ),
    Action(
        action_type="attack", alignment="corrupt", title="Devassa Fiscal Seletiva",
        description="Suborna fiscais para multar pesadamente empresas apoiadoras do rival político.",
        risk_level="high",
        responses={"high_critical": "Redes de financiamento do rival colapsam sob multas pesadas.", "normal_success": "Constrangimento afasta doadores do oponente.", "normal_fail": "Auditores honestos denunciam a perseguição fiscal.", "low_critical": "Empresários processam o Estado por extorsão e vencem."}
    ),
    Action(
        action_type="attack", alignment="corrupt", title="Assédio a Redutos Eleitorais",
        description="Com uso de caixa dois, distribui dinheiro em troca da exclusão de comícios rivais.",
        risk_level="medium",
        responses={"high_critical": "Domina votos em comunidades carentes usando dinheiro vivo.", "normal_success": "Garante lealdade momentânea comprada com grana.", "normal_fail": "População pega o dinheiro mas vai ao comício rival mesmo assim.", "low_critical": "Fiscalização eleitoral filma a distribuição de dinheiro."}
    ),
    Action(
        action_type="attack", alignment="corrupt", title="Sabotagem de Infraestrutura de Votação",
        description="Valendo-se de vândalos contratados, danifica locais de votação em zonas do oponente.",
        risk_level="high",
        responses={"high_critical": "Provoca abstenção maciça nos redutos do rival.", "normal_success": "Atrasa a votação na base oponente usando sabotagem paga.", "normal_fail": "Autoridades consertam os estragos rapidamente.", "low_critical": "Vândalos presos confessam que receberam dinheiro seu."}
    ),
    Action(
        action_type="attack", alignment="corrupt", title="Espionagem Interna de Gabinete",
        description="Suborna assessores diretos da equipe do oponente para obter segredos estratégicos.",
        risk_level="medium",
        responses={"high_critical": "Antecipa cada passo e estratégia comprada do rival.", "normal_success": "Obtém planos confidenciais pagos por fora.", "normal_fail": "O informante cobrou caro e entregou dados inúteis.", "low_critical": "O suborno é gravado e entregue à polícia."}
    ),
    Action(
        action_type="attack", alignment="corrupt", title="Coação de Testemunhas-Chave",
        description="Oferece suborno volumoso para testemunhas mudarem depoimentos em processos rivais.",
        risk_level="high",
        responses={"high_critical": "Testemunhas vendem o silêncio e os processos caem.", "normal_success": "Atrasa investigações usando dinheiro e pressão.", "normal_fail": "O ministério público protege a testemunha das ofertas.", "low_critical": "A tentativa de suborno vira prova de obstrução de justiça."}
    ),
    Action(
        action_type="attack", alignment="corrupt", title="Vazamento de Material Privado",
        description="Compra registros comprometedores da vida pessoal de opositores para chantagem.",
        risk_level="high",
        responses={"high_critical": "Destrói a reputação do rival com material caríssimo.", "normal_success": "Força o oponente a se esconder de debates.", "normal_fail": "O oponente contorna o escândalo sem maiores danos.", "low_critical": "O fornecedor do material vaza que foi você quem pagou."}
    ),
    Action(
        action_type="attack", alignment="corrupt", title="Censura Judicial Induzida",
        description="Paga advogados caros para tentar calar jornais e portais críticos.",
        risk_level="high",
        responses={"high_critical": "Abafa investigações comprometedoras usando o poder do dinheiro.", "normal_success": "Silencia críticos incômodos na base de processos.", "normal_fail": "Tribunais superiores derrubam as liminares pagas.", "low_critical": "O esforço judicial custa uma fortuna e sai pela culatra."}
    ),
    Action(
        action_type="attack", alignment="corrupt", title="Inflação Artificial de Indicadores",
        description="Paga institutos de fachada para inventar pesquisas que te favorecem e desmoralizam o rival.",
        risk_level="low",
        responses={"high_critical": "Atrai investidores e doadores de dinheiro com a farsa.", "normal_success": "Cria uma percepção falsa de favoritismo comprado.", "normal_fail": "Levantamentos sérios desmentem os números pagos.", "low_critical": "A fraude estatística é exposta e custa caro."}
    ),
    Action(
        action_type="attack", alignment="corrupt", title="Armação de Denúncias Falsas",
        description="Mediante pagamento de cachê, contrata atores para registrarem falsas queixas policiais contra o rival.",
        risk_level="medium",
        responses={"high_critical": "Oponente gasta rios de dinheiro se defendendo na polícia.", "normal_success": "Mancha a imagem do rival usando denúncias pagas.", "normal_fail": "Furos óbvios desmascaram a encenação dos atores.", "low_critical": "Atores expõem o cachê que receberam para mentir."}
    ),
    Action(
        action_type="attack", alignment="corrupt", title="Interceptação Clandestina",
        description="Contrata espiões do submundo para grampear telefones de ministros rivais.",
        risk_level="high",
        responses={"high_critical": "Consegue informações valiosas compradas no submundo.", "normal_success": "Acumula segredos úteis obtidos por espionagem paga.", "normal_fail": "Sistemas de segurança detectam a invasão cara.", "low_critical": "A central de espionagem é estourada pela polícia."}
    ),
    Action(
        action_type="attack", alignment="corrupt", title="Proscrição Digital de Opositores",
        description="Suborna intermediários para derrubar canais e redes sociais do rival.",
        risk_level="medium",
        responses={"high_critical": "Corta a comunicação digital do rival com dinheiro.", "normal_success": "Enfraquece a campanha online do oponente.", "normal_fail": "Plataformas rejeitam os bloqueios injustificados.", "low_critical": "O esquema de propina digital é descoberto e punido."}
    ),
    Action(
        action_type="attack", alignment="corrupt", title="Roubo e Vazamento de Cadastros",
        description="Com ataque hacker patrocinado, expõe dados sigilosos de doadores da oposição.",
        risk_level="high",
        responses={"high_critical": "Intimida doadores ricos a cortarem verbas do rival.", "normal_success": "Seca o financiamento de campanha do oponente.", "normal_fail": "Bases de dados contavam com criptografia inviolável.", "low_critical": "A fatura paga ao hacker é rastreada até suas contas."}
    ),
    Action(
        action_type="attack", alignment="corrupt", title="Confisco Arbitrário de Ativos",
        description="Através de decretos arbitrários, bloqueia recursos financeiros de grupos rivais.",
        risk_level="high",
        responses={"high_critical": "Paralisa totalmente a logística e os gastos do oponente.", "normal_success": "Impossibilita o rival de pagar fornecedores de campanha.", "normal_fail": "O judiciário suspende o confisco ilegal de dinheiro.", "low_critical": "Tribunais punem o Estado por roubo de ativos."}
    ),
    Action(
        action_type="attack", alignment="corrupt", title="Milícias de Desinformação Coordenada",
        description="Financia exércitos de robôs e perfis pagos para espalhar mentiras destrutivas.",
        risk_level="medium",
        responses={"high_critical": "Inunda redes com mentiras pagas que destroem o oponente.", "normal_success": "Gera ruído e desconfiança usando dinheiro nas redes.", "normal_fail": "As plataformas bloqueiam a rede paga de robôs.", "low_critical": "O financiamento da milícia digital é descoberto e exposto."}
    ),
    Action(
        action_type="attack", alignment="corrupt", title="Compra de Apoio Parlamentar em Bloco",
        description="Oferece suborno e cargos para desfalcar a bancada legislativa do oponente.",
        risk_level="high",
        responses={"high_critical": "Destrói a coesão da oposição comprando seus aliados.", "normal_success": "Assegura maioria absoluta com parlamentares alugados.", "normal_fail": "Parlamentares pegam o dinheiro e votam contra mesmo assim.", "low_critical": "A negociação de compra de votos vaza em vídeo."}
    ),
    Action(
        action_type="attack", alignment="corrupt", title="Sabotagem Física de Eventos",
        description="Contrata baderneiros profissionais para destruírem e cancelarem atos do oponente.",
        risk_level="high",
        responses={"high_critical": "Espalha pânico e esvazia comícios pagos da oposição.", "normal_success": "Força o cancelamento de agendas caras do rival.", "normal_fail": "A segurança do evento expulsa os vândalos contratados.", "low_critical": "Vândalos presos confessam o pagamento que receberam de você."}
    ),
    Action(
        action_type="attack", alignment="corrupt", title="Disseminação de Boatos sobre Saúde",
        description="Paga falsos médicos para inventarem diagnósticos graves sobre o rival.",
        risk_level="low",
        responses={"high_critical": "Investidores retiram dinheiro do oponente achando que ele vai falhar.", "normal_success": "Desvia o foco usando boatos caros.", "normal_fail": "Oponente faz exames públicos que desmentem o boato pago.", "low_critical": "Descobrem que a junta médica falsa foi paga por você."}
    ),
    Action(
        action_type="attack", alignment="corrupt", title="Simulação de Crise de Segurança",
        description="Contrata pirotécnicos para criar falsas explosões e culpar o rival na mídia.",
        risk_level="high",
        responses={"high_critical": "Cria pânico generalizado e suga verbas de segurança.", "normal_success": "Desvia a atenção de escândalos financeiros recentes.", "normal_fail": "Perícia descobre que a explosão foi simulada.", "low_critical": "O fogo fora de controle destrói patrimônio e gera processo."}
    ),
    Action(
        action_type="attack", alignment="corrupt", title="Demissão de Críticos Acadêmicos",
        description="Usa pressões financeiras e doações condicionadas para calar pesquisadores rivais.",
        risk_level="medium",
        responses={"high_critical": "Elimina estudos independentes que expõem seus desvios.", "normal_success": "Cria silêncio acadêmico comprado.", "normal_fail": "Universidades rejeitam a chantagem financeira.", "low_critical": "O caso de compra de silêncio vira escândalo internacional."}
    ),
    Action(
        action_type="attack", alignment="corrupt", title="Uso Político de Credos",
        description="Suborna lideranças religiosas para pregarem contra a honestidade moral do rival.",
        risk_level="high",
        responses={"high_critical": "Destrói o capital político do oponente em templos financiados.", "normal_success": "Isola o rival de bases conservadoras usando suborno.", "normal_fail": "Fiéis rejeitam a compra de votos nos altares.", "low_critical": "O líder religioso pego com dinheiro propõe delação."}
    ),
    Action(
        action_type="attack", alignment="corrupt", title="Difusão de Alertas Falsos Internacionais",
        description="Paga lobistas estrangeiros para espalhar relatórios falsos contra o rival no exterior.",
        risk_level="medium",
        responses={"high_critical": "Isola o oponente de apoios diplomáticos pagos.", "normal_success": "Atrapalha acordos internacionais do rival.", "normal_fail": "Embaixadas ignoram os relatórios por falta de provas.", "low_critical": "A farsa internacional é descoberta e gera multa pesada."}
    ),
    Action(
        action_type="attack", alignment="corrupt", title="Bloqueio Logístico Regional",
        description="Paga empresas de transporte para boicotarem as caravanas do oponente.",
        risk_level="high",
        responses={"high_critical": "Impossibilita o oponente de viajar e fazer comícios.", "normal_success": "Desmobiliza a militância rival usando bloqueios pagos.", "normal_fail": "Forças federais liberam as estradas rapidamente.", "low_critical": "Apropriação indébita das frotas gera inquérito."}
    ),
    Action(
        action_type="attack", alignment="corrupt", title="Devassa de Sigilos Bancários",
        description="Suborna funcionários bancários corrompidos para acessar contas privadas do rival.",
        risk_level="high",
        responses={"high_critical": "Descobre onde o oponente guarda suas economias e desvios.", "normal_success": "Mapeia o dinheiro privado do rival para chantagem.", "normal_fail": "Sistemas bancários registram a invasão comprada.", "low_critical": "Funcionário corrupto confessa que vendeu os dados a você."}
    ),
    Action(
        action_type="attack", alignment="corrupt", title="Manipulação de Pauta em Tribunais",
        description="Paga propina a intermediários para acelerar artificialmente processos contra o rival.",
        risk_level="high",
        responses={"high_critical": "Inabilita o oponente usando decisões judiciais compradas.", "normal_success": "Mantém o rival sufocado por processos caros.", "normal_fail": "Tribunal superior anula a pressa comprada.", "low_critical": "Magistrados caem em operação por receber propina sua."}
    ),
    Action(
        action_type="attack", alignment="corrupt", title="Restrição de Cadastros Eleitorais",
        description="Financia barreiras burocráticas pagas para impedir o voto em zonas rivais.",
        risk_level="medium",
        responses={"high_critical": "Reduz o colégio eleitoral opositor usando artifícios caros.", "normal_success": "Diminui a margem contrária em votações cruciais.", "normal_fail": "Órgãos anulam as barreiras e liberam os cadastros.", "low_critical": "Partido condenado por gastar para barrar eleitores."}
    ),
    Action(
        action_type="attack", alignment="corrupt", title="Invasão e Roubo de Acervos",
        description="Paga criminosos para roubarem o cofre e o financeiro do comitê rival.",
        risk_level="high",
        responses={"high_critical": "Rouba todo o dinheiro em espécie e dados da oposição.", "normal_success": "Desorganiza a campanha rival na reta final.", "normal_fail": "Segurança armada impede os criminosos pagos.", "low_critical": "Criminosos presos confessam que foram pagos por você."}
    ),
    Action(
        action_type="attack", alignment="corrupt", title="Armadilha de Flagrante Forjado",
        description="Suborna policiais corruptos para plantarem provas e prenderem o rival.",
        risk_level="high",
        responses={"high_critical": "Remove o principal nome da oposição com uma prisão comprada.", "normal_success": "Mancha a reputação do rival com um flagrante arranjado.", "normal_fail": "Câmeras de segurança registram a propina dada aos policiais.", "low_critical": "A armação é descoberta e resulta em sua própria prisão."}
    ),
    Action(
        action_type="attack", alignment="corrupt", title="Asfixia Orçamentária de Órgãos Rivais",
        description="Corta repasses financeiros para prefeituras chefiadas por opositores em retaliação.",
        risk_level="high",
        responses={"high_critical": "Paralisa a administração rival por falta de dinheiro.", "normal_success": "Sufoca o orçamento da prefeitura oponente.", "normal_fail": "Tribunais restabelecem os repasses financeiros forçados.", "low_critical": "Sua própria base sofre com cortes de retaliação."}
    ),
    Action(
        action_type="attack", alignment="corrupt", title="Intimidação de Equipes Contábeis",
        description="Paga capangas para ameaçarem os contadores que auditam o rival.",
        risk_level="medium",
        responses={"high_critical": "Deixa o oponente sem assessoria por medo de violência.", "normal_success": "Atrasa as contas de campanha do rival com ameaças pagas.", "normal_fail": "Contadores denunciam a intimidação às autoridades.", "low_critical": "O esquema de capangas pagos vira manchete policial."}
    ),
    Action(
        action_type="attack", alignment="corrupt", title="Bloqueio de Praças Públicas",
        description="Paga propina à prefeitura para reservar todos os espaços antes do rival.",
        risk_level="medium",
        responses={"high_critical": "Impossibilita o oponente de fazer comícios nas praças principais.", "normal_success": "Obriga o rival a gastar o dobro em locais distantes.", "normal_fail": "Prefeitura anula as reservas fraudulentas.", "low_critical": "A propina das reservas é descoberta e anulada."}
    ),
    Action(
        action_type="attack", alignment="corrupt", title="Simulação de Agressão Pública",
        description="Paga figurantes para simularem um ataque contra você e culparem o rival.",
        risk_level="low",
        responses={"high_critical": "Comoção nacional com o falso ataque catapulta sua campanha.", "normal_success": "Monopoliza a mídia com o teatro pago.", "normal_fail": "Perícia prova que os ferimentos dos figurantes eram falsos.", "low_critical": "O cachê pago aos figurantes vaza na internet."}
    ),
    Action(
        action_type="attack", alignment="corrupt", title="Coação de Financiadores Rivais",
        description="Usa ameaças financeiras pesadas para assustar quem doa dinheiro ao oponente.",
        risk_level="medium",
        responses={"high_critical": "Seca totalmente o dinheiro de campanha da oposição.", "normal_success": "Reduz drasticamente os atos caros do rival.", "normal_fail": "Empresários ignoram as ameaças e dobram as doações.", "low_critical": "Associações denunciam sua extorsão financeira."}
    ),
    Action(
        action_type="attack", alignment="corrupt", title="Ataques de Negação de Serviço",
        description="Contrata hackers caros para derrubar os sites e doações online do rival.",
        risk_level="low",
        responses={"high_critical": "Corta a arrecadação online e a comunicação do oponente.", "normal_success": "Gera instabilidade financeira na campanha digital rival.", "normal_fail": "O rival usa servidores blindados contra o ataque hacker.", "low_critical": "O rastreio do pagamento ao hacker aponta para você."}
    ),
    Action(
        action_type="attack", alignment="corrupt", title="Falsificação de Registros Partidários",
        description="Suborna cartórios para forjar documentos que cassem a legenda rival.",
        risk_level="low",
        responses={"high_critical": "Cria crise jurídica cara que quase cassa a chapa oponente.", "normal_success": "Gera dor de cabeça judicial com documentos falsos pagos.", "normal_fail": "Perito descobre a falsificação cartorária em segundos.", "low_critical": "Cartório envolvido confessa a propina recebida."}
    ),
    Action(
        action_type="attack", alignment="corrupt", title="Destruição de Recursos Logísticos Opositores",
        description="Paga criminosos para incendiarem os carros de som da campanha rival.",
        risk_level="high",
        responses={"high_critical": "Imobiliza a estrutura de som e propaganda do rival.", "normal_success": "Atrapalha a agenda de rua do candidato oponente.", "normal_fail": "Segurança flagra o incêndio criminoso a tempo.", "low_critical": "Criminosos presos entregam quem pagou pelo serviço."}
    ),
    Action(
        action_type="attack", alignment="corrupt", title="Extorsão a Prefeitos Aliados do Rival",
        description="Ameaça cortar verbas de prefeituras se não abandonarem o oponente político.",
        risk_level="medium",
        responses={"high_critical": "Isola o candidato rival cortando suas fontes de recursos locais.", "normal_success": "Enfraquece a capilaridade financeira do oponente.", "normal_fail": "Prefeitos rejeitam a chantagem e expõem a ameaça.", "low_critical": "Prefeitos aliados abandonam você por excesso de achaque."}
    ),
    Action(
        action_type="attack", alignment="corrupt", title="Litigância Internacional Falsa",
        description="Contrata advogados caros para abrir processos absurdos e caros no exterior.",
        risk_level="low",
        responses={"high_critical": "Gera custos astronômicos de defesa para o oponente.", "normal_success": "Atrapalha a imagem internacional do rival com processos pagos.", "normal_fail": "Tribunais estrangeiros rejeitam e multam os advogados.", "low_critical": "A farra dos processos caros se volta contra seu orçamento."}
    ),
    Action(
        action_type="attack", alignment="corrupt", title="Contaminação de Eventos Opositores",
        description="Paga vândalos para jogarem substâncias fétidas nos comícios rivais.",
        risk_level="low",
        responses={"high_critical": "Esvazia comícios e sabota os eventos caros do oponente.", "normal_success": "Incomoda o público e estraga o discurso do rival.", "normal_fail": "Participantes ignoram o mau cheiro e continuam no ato.", "low_critical": "Vândalos contratados são pegos com o dinheiro no bolso."}
    ),
     Action(
        action_type="attack", alignment="good", title="Quebra de Monopólio Farmacêutico",
        description="Autoriza genéricos com rigor normativo para forçar a redução de preços abusivos.",
        risk_level="medium",
        responses={"high_critical": "Garante acesso popular a tratamentos essenciais e enfraquece cartéis.", "normal_success": "Barateia medicamentos fundamentais nas redes públicas.", "normal_fail": "Lobbies industriais suspendem distribuição temporariamente.", "low_critical": "Barreiras comerciais internacionais travam as importações."}
    ),
    Action(
        action_type="attack", alignment="good", title="Transparência em Comissão Parlamentar",
        description="Transmite integralmente investigações públicas que o governo tentava ocultar.",
        risk_level="low",
        responses={"high_critical": "Consciência pública em massa pressiona e desgasta a base corrupta.", "normal_success": "Atrai atenção nacional para irregularidades graves.", "normal_fail": "Assuntos excessivamente técnicos dispersam a audiência.", "low_critical": "Erros de comunicação geram memes desfavoráveis."}
    ),
    Action(
        action_type="attack", alignment="good", title="Auditoria Contábil Implacável",
        description="Revela desvios e superfaturamentos através de exames detalhados em contratos públicos.",
        risk_level="medium",
        responses={"high_critical": "Comprova irregularidades e paralisa pagamentos ilegais na hora.", "normal_success": "Expõe a fragilidade administrativa do oponente.", "normal_fail": "Tribunais aliados do governo validam os contratos.", "low_critical": "Falhas na auditoria técnica desacreditam o relatório."}
    ),
    Action(
        action_type="attack", alignment="good", title="Mapeamento de Nepotismo",
        description="Publica a lista completa de parentes nomeados em gabinetes públicos.",
        risk_level="low",
        responses={"high_critical": "Obriga a exoneração imediata de dezenas de parentes instalados.", "normal_success": "Constrange a administração com dados irrefutáveis.", "normal_fail": "Nomes apontados eram concursados de carreira legítima.", "low_critical": "Descobre-se um caso similar em sua própria trajetória."}
    ),
    Action(
        action_type="attack", alignment="good", title="Ação Direta de Inconstitucionalidade",
        description="Interrompe decretos arbitrários por meio de recursos no Supremo Tribunal.",
        risk_level="high",
        responses={"high_critical": "Suspende medidas arbitrárias e impõe derrota institucional ao rival.", "normal_success": "Garante a vigência das salvaguardas constitucionais.", "normal_fail": "Tribunal adia a análise com pedidos de vista prolongados.", "low_critical": "Supremo valida a norma e legitima as ações do oponente."}
    ),
    Action(
        action_type="attack", alignment="good", title="Mobilização Comunitária de Base",
        description="Organiza protestos pacíficos para barrar a venda de patrimônio público.",
        risk_level="medium",
        responses={"high_critical": "Força o Executivo a recuar diante da pressão popular organizada.", "normal_success": "Coloca o tema no centro do debate público regional.", "normal_fail": "Baixa adesão esvazia o impacto do protesto.", "low_critical": "Infiltrados promovem quebra-quebra, invalidando o ato."}
    ),
    Action(
        action_type="attack", alignment="good", title="Delação Premiada Colaborativa",
        description="Incentiva agentes arrependidos a revelarem esquemas de corrupção com amparo legal.",
        risk_level="high",
        responses={"high_critical": "Fornece provas materiais incontestáveis que derrubam a cúpula rival.", "normal_success": "Gera inquéritos consistentes contra gestores corruptos.", "normal_fail": "Acordos falham por falta de cooperação dos réus.", "low_critical": "Vazamentos indevidos comprometem a validade das provas."}
    ),
    Action(
        action_type="attack", alignment="good", title="Campanha de Consumo Consciente",
        description="Orienta boicotes legítimos contra empresas financiadoras de ilegalidades.",
        risk_level="medium",
        responses={"high_critical": "Prejuízos de imagem forçam corporações a cortarem apoios ilícitos.", "normal_success": "Conscientiza o mercado consumidor sobre responsabilidade.", "normal_fail": "Consumidores priorizam preços baixos e ignoram o selo.", "low_critical": "Empresas processam organizadores por difamação comercial."}
    ),
    Action(
        action_type="attack", alignment="good", title="Plataforma de Monitoramento de Promessas",
        description="Lança portal interativo expondo atrasos e mentiras em planos de governo.",
        risk_level="low",
        responses={"high_critical": "Desmascara o discurso oficial com dados claros e viraliza.", "normal_success": "Mantém o oponente na defensiva durante os debates.", "normal_fail": "Falta de manutenção desatualiza a plataforma.", "low_critical": "O oponente usa a ferramenta para justificar atrasos complexos."}
    ),
    Action(
        action_type="attack", alignment="good", title="Debates Abertos com a Sociedade",
        description="Obriga candidatos a responderem diretamente a questionamentos populares.",
        risk_level="medium",
        responses={"high_critical": "Expõe o distanciamento da classe política tradicional.", "normal_success": "Humaniza o debate com demandas reais da população.", "normal_fail": "Candidatos da máquina esquivam-se dos encontros.", "low_critical": "Perguntas direcionadas geram confusão e bate-boca."}
    ),
    Action(
        action_type="attack", alignment="good", title="Congelamento Judicial de Ativos Ilícitos",
        description="Obtém bloqueio preventivo de recursos suspeitos através da justiça.",
        risk_level="high",
        responses={"high_critical": "Asfixia a capacidade financeira de redes corruptas rapidamente.", "normal_success": "Interrompe a circulação de capitais de origem duvidosa.", "normal_fail": "Bancos estrangeiros retardam o cumprimento da ordem.", "low_critical": "Bloqueio atinge contas regulares por erro de homônimo."}
    ),
    Action(
        action_type="attack", alignment="good", title="Ação Popular de Improbidade",
        description="Move processos judiciais embasados em evidências de uso incorreto da máquina pública.",
        risk_level="high",
        responses={"high_critical": "Resulta na cassação e inelegibilidade de gestores infiéis.", "normal_success": "Gera desgaste jurídico profundo na campanha rival.", "normal_fail": "Juízos locais arquivam as petições preliminarmente.", "low_critical": "A ação é julgada leviana e acarreta ônus financeiro."}
    ),
    Action(
        action_type="attack", alignment="good", title="Perícia Técnica Independente",
        description="Contrata especialistas para atestar falhas em obras públicas superfaturadas.",
        risk_level="medium",
        responses={"high_critical": "Comprova fraudes estruturais irrefutáveis na engenharia.", "normal_success": "Desmente laudos oficiais encomendados.", "normal_fail": "Custos elevados esgotam o orçamento da pesquisa.", "low_critical": "Peritos cometem erros metodológicos graves."}
    ),
    Action(
        action_type="attack", alignment="good", title="Greve Geral Articulada",
        description="Coordena paralisação de setores produtivos contra retrocessos com amparo sindical.",
        risk_level="high",
        responses={"high_critical": "Paralisa a economia e obriga o governo a revogar medidas abusivas.", "normal_success": "Constrange o legislativo a negociar pautas populares.", "normal_fail": "Setores essenciais furam a paralisação por pressões.", "low_critical": "Governo endurece repressão policial contra os grevistas."}
    ),
    Action(
        action_type="attack", alignment="good", title="Denúncia em Cortes Internacionais",
        description="Leva registros de violações institucionais a tribunais globais com respaldo jurídico.",
        risk_level="high",
        responses={"high_critical": "Gera condenações que constrangem o país e forçam recuos legais.", "normal_success": "Atrai holofotes internacionais para abusos internos.", "normal_fail": "Trâmites burocráticos arrastam-se por anos sem efeito.", "low_critical": "Governo usa denúncias para inflamar discurso ufanista."}
    ),
    Action(
        action_type="attack", alignment="good", title="Exposição de Conflito de Interesses",
        description="Revela vínculos empresariais ocultos de autoridades em gabinetes públicos.",
        risk_level="medium",
        responses={"high_critical": "Força a renúncia imediata de ministros e secretários expostos.", "normal_success": "Alimenta investigações de comissões de ética.", "normal_fail": "Autoridades alegam transferência de gestão para fundos cegos.", "low_critical": "Processo por divulgar participações societárias legais."}
    ),
    Action(
        action_type="attack", alignment="good", title="Marcha Cidadã pela Democracia",
        description="Reúne multidões em atos pacíficos em defesa da segurança constitucional.",
        risk_level="low",
        responses={"high_critical": "Demonstração massiva de força cívica que inibe arroubos autoritários.", "normal_success": "Mantém viva a mobilização popular nas ruas.", "normal_fail": "Condições climáticas adversas esvaziam o ato.", "low_critical": "Vandalismo isolado desvia o foco da pauta principal."}
    ),
    Action(
        action_type="attack", alignment="good", title="Abaixo-Assinado de Iniciativa Popular",
        description="Coleta milhões de assinaturas reais para protocolar projetos anticorrupção.",
        risk_level="medium",
        responses={"high_critical": "Constrange o parlamento a votar leis de combate à impunidade.", "normal_success": "Insere pautas legítimas na agenda legislativa obrigatória.", "normal_fail": "Mesas diretoras engavetam as caixas de petições.", "low_critical": "Invalidam assinaturas por falhas formais de cadastro."}
    ),
    Action(
        action_type="attack", alignment="good", title="Plebiscito sobre Concessões",
        description="Convoca consulta pública para decidir democraticamente sobre privatizações.",
        risk_level="high",
        responses={"high_critical": "Garante soberania popular direta sobre ativos estratégicos.", "normal_success": "Suspende temporariamente as vendas sob contestação.", "normal_fail": "Legislativo altera leis para proibir a realização do plebiscito.", "low_critical": "Campanha corporativa reverte o resultado nas urnas."}
    ),
    Action(
        action_type="attack", alignment="good", title="Paralisação Setorial Estratégica",
        description="Coordena interrupção de serviços com preceitos legais para frear pacotes nocivos.",
        risk_level="high",
        responses={"high_critical": "Imobiliza a governabilidade e força acordos imediatos.", "normal_success": "Demonstra o poder de articulação das bases trabalhistas.", "normal_fail": "Falta de solidariedade entre categorias enfraquece o ato.", "low_critical": "Governo declara ilegalidade e aplica multas pesadas."}
    ),
    Action(
        action_type="attack", alignment="good", title="Comitê de Apoio a Vítimas de Desastres",
        description="Dá visibilidade jurídica e social a comunidades negligenciadas por gestões.",
        risk_level="low",
        responses={"high_critical": "Atrai solidariedade nacional e garante reparações judiciais rápidas.", "normal_success": "Mantém o foco na responsabilidade civil dos governantes.", "normal_fail": "Empresas rés oferecem acordos sigilosos para abafar o caso.", "low_critical": "Vítimas são instrumentalizadas politicamente e abandonadas."}
    ),
    Action(
        action_type="attack", alignment="good", title="Vigília Cívica Permanente",
        description="Mantém presença pacífica e vigilante em frente a sedes de poderes republicanos.",
        risk_level="medium",
        responses={"high_critical": "Inibe votações noturnas surpresa de projetos danosos.", "normal_success": "Sinaliza atenção constante da sociedade civil organizada.", "normal_fail": "Forças de segurança dispersam o acampamento com gás.", "low_critical": "Confrontos noturnos mancham a imagem do movimento."}
    ),
    Action(
        action_type="attack", alignment="good", title="Painel Público de Desperdício",
        description="Instala contadores visíveis de recursos públicos alocados de forma incorreta.",
        risk_level="low",
        responses={"high_critical": "Constrangimento contínuo pressiona administradores a explicarem rombos.", "normal_success": "Informa pedestres sobre a eficiência dos gastos.", "normal_fail": "Prefeituras mandam desligar sob alegação de poluição visual.", "low_critical": "Equipamentos sofrem vandalismo e são destruídos."}
    ),
    Action(
        action_type="attack", alignment="good", title="Entrevista Reveladora em Rede Nacional",
        description="Apresenta provas documentais irrefutáveis ao público em horário nobre.",
        risk_level="high",
        responses={"high_critical": "Choca a opinião pública e acelera investigações adormecidas.", "normal_success": "Domina o noticiário político da semana inteira.", "normal_fail": "Emissoras tentam diluir o impacto com contra-argumentos.", "low_critical": "Nervosismo compromete a clareza da exposição das provas."}
    ),
    Action(
        action_type="attack", alignment="good", title="Frente Ampliada Suprapartidária",
        description="Une correntes ideológicas diversas em torno de pautas republicanas de integridade.",
        risk_level="high",
        responses={"high_critical": "Isola radicalismos e aprova salvaguardas institucionais históricas.", "normal_success": "Garante ampla maioria em votações de interesse cívico.", "normal_fail": "Divergências internas implodem a coalizão rapidamente.", "low_critical": "Apoiadores radicais acusam você de traição ideológica."}
    ),
    Action(
        action_type="attack", alignment="good", title="Resistência Fiscal Coletiva",
        description="Orienta suspensão temporária de taxas abusivas com sólido respaldo jurídico.",
        risk_level="high",
        responses={"high_critical": "Asfixia a arrecadação de governos que praticam extorsão fiscal.", "normal_success": "Conquista apoio maciço do setor comercial afetado.", "normal_fail": "Fisco estadual aplica multas e executa dívidas rapidamente.", "low_critical": "Tribunais consideram a orientação ilegal e punem líderes."}
    ),
    Action(
        action_type="attack", alignment="good", title="Rastreamento Ciberforense de Criptoativos",
        description="Mapeia o fluxo tecnológico de moedas digitais usadas em propinas com peritos.",
        risk_level="medium",
        responses={"high_critical": "Identifica as carteiras finais de beneficiários de esquemas.", "normal_success": "Fornece indícios valiosos para o ministério público.", "normal_fail": "Tecnologia complexa é ignorada por tribunais tradicionais.", "low_critical": "Hackers alvos destroem os rastros antes da apreensão."}
    ),
    Action(
        action_type="attack", alignment="good", title="Ocupação Cívica de Prédios Abandonados",
        description="Destina imóveis públicos ociosos para funções sociais amparadas por lei.",
        risk_level="medium",
        responses={"high_critical": "Expõe o descaso patrimonial e força soluções habitacionais.", "normal_success": "Conquista simpatia popular para a causa urbana.", "normal_fail": "Forças de segurança executam despejo sumário.", "low_critical": "Conflitos na reintegração prejudicam a imagem do grupo."}
    ),
    Action(
        action_type="attack", alignment="good", title="Notificação Técnica ao Tribunal de Contas",
        description="Protocolar dossiês de irregularidades com evidências técnicas irrefutáveis.",
        risk_level="low",
        responses={"high_critical": "Corte de contas suspende repasses sob suspeita imediatamente.", "normal_success": "Trava pagamentos imorais de empreiteiras.", "normal_fail": "Tribunal engaveta o documento por excesso de demandas.", "low_critical": "Erros formais na notificação invalidam o processo."}
    ),
    Action(
        action_type="attack", alignment="good", title="Campanha de Desfiliação Ética",
        description="Promove debandada pública de quadros partidários após comprovação de escândalos.",
        risk_level="medium",
        responses={"high_critical": "Desmoraliza legendas envolvidas em corrupção sistemática.", "normal_success": "Filtra e limpa o espectro de apoios políticos.", "normal_fail": "Políticos acusados apegam-se aos cargos e ignoram a saída.", "low_critical": "Seu próprio grupo sofre divisões internas por disputas."}
    ),
    Action(
        action_type="attack", alignment="good", title="Caravana Cívica pelo Interior",
        description="Percorre municípios distantes para fiscalizar in loco (no local) os serviços públicos.",
        risk_level="low",
        responses={"high_critical": "Expõe o abandono estatal e mobiliza comunidades esquecidas.", "normal_success": "Constrói capilaridade política legítima baseada em fatos.", "normal_fail": "Problemas logísticos impedem o cronograma de visitas.", "low_critical": "Prefeituras locais sabotam a recepção da caravana."}
    ),
    Action(
        action_type="attack", alignment="good", title="Financiamento Coletivo Transparente",
        description="Arrecada fundos de campanha exclusivamente de microdoadores reais auditados.",
        risk_level="medium",
        responses={"high_critical": "Garante independência total de grandes grupos de interesse.", "normal_success": "Demonstra capilaridade e apoio orgânico real.", "normal_fail": "Volume arrecadado fica abaixo das expectativas logísticas.", "low_critical": "Plataforma de doação sofre falha sistêmica e trava."}
    ),
    Action(
        action_type="attack", alignment="good", title="Ação Civil Pública Ambiental",
        description="Protege ecossistemas ameaçados com rigorosas interdições judiciais urgentes.",
        risk_level="high",
        responses={"high_critical": "Embarga desmatamentos ilegais antes de danos irreversíveis.", "normal_success": "Salva áreas de preservação da especulação predatória.", "normal_fail": "Juízes locais cassam as liminares ambientais.", "low_critical": "Canteiros de obras operam ilegalmente à revelia da justiça."}
    ),
    Action(
        action_type="attack", alignment="good", title="Mapeamento Voluntário de Obras Ociosas",
        description="Cria inventário digital colaborativo de construções públicas abandonadas.",
        risk_level="low",
        responses={"high_critical": "Constrói base de dados inquestionável sobre o desperdício estatal.", "normal_success": "Fornece munição técnica para debates e cobranças.", "normal_fail": "Governo atual culpa gestões anteriores pelo abandono.", "low_critical": "Equipe técnica sofre ameaças de grupos ligados às obras."}
    ),
    Action(
        action_type="attack", alignment="good", title="Publicação de Folhas de Pagamento Sigilosas",
        description="Expõe privilégios e supersalários ocultos no funcionalismo de elite com dados oficiais.",
        risk_level="high",
        responses={"high_critical": "Gera revolta pública capaz de forçar reformas moralizadoras.", "normal_success": "Joga luz sobre gastos corporativos inaceitáveis.", "normal_fail": "Tribunais alegam proteção de dados para barrar divulgações.", "low_critical": "Responsáveis pelo vazamento enfrentam processos disciplinares."}
    ),
    Action(
        action_type="attack", alignment="good", title="Programa de Proteção a Denunciantes",
        description="Oferece suporte jurídico integral a servidores que expõem fraudes e desvios.",
        risk_level="medium",
        responses={"high_critical": "Incentiva revelações internas de esquemas bem protegidos.", "normal_success": "Garante segurança a quem decide falar a verdade.", "normal_fail": "Denunciantes sofrem retaliações administrativas veladas.", "low_critical": "Informações reveladas mostram-se imprecisas."}
    ),
    Action(
        action_type="attack", alignment="good", title="Articulação com Redes Globais de Imprensa",
        description="Fornece dados verificados a consórcios internacionais de jornalismo investigativo.",
        risk_level="high",
        responses={"high_critical": "Coloca escândalos locais sob os holofotes da imprensa mundial.", "normal_success": "Evita abafamentos institucionais domésticos.", "normal_fail": "Veículos internacionais consideram o tema de alcance restrito.", "low_critical": "Governo classifica a articulação como campanha difamatória externa."}
    ),
    Action(
        action_type="attack", alignment="good", title="Comissão Cidadã Independente",
        description="Cria comitê técnico autônomo para fiscalizar gastos emergenciais públicos.",
        risk_level="high",
        responses={"high_critical": "Garante lisura (honestidade) e impede desvios em contratos excepcionais.", "normal_success": "Oferece pareceres técnicos imparciais à sociedade.", "normal_fail": "Gestores públicos ignoram as recomendações do comitê.", "low_critical": "Falta de orçamento contínuo encerra as atividades."}
    ),
    Action(
        action_type="attack", alignment="good", title="Panelaço Cívico Sincronizado",
        description="Coordena protesto acústico urbano com engajamento popular contra desmandos.",
        risk_level="low",
        responses={"high_critical": "Demonstra rejeição popular estrondosa e imediata à gestão.", "normal_success": "Unifica comunidades em um recado direto aos governantes.", "normal_fail": "Protesto dura poucos minutos e perde força.", "low_critical": "Manifestação fraca é usada por governistas para demonstrar força."}
    ),
    Action(
        action_type="attack", alignment="good", title="Selo de Integridade Comercial",
        description="Certifica empresas probas (honestas) que recusam redes de corrupção corporativa.",
        risk_level="medium",
        responses={"high_critical": "Atrai consumidores conscientes e fortalece o mercado probo.", "normal_success": "Diferencia empresas honestas da concorrência viciada.", "normal_fail": "Baixa adesão corporativa inicial limita o alcance do selo.", "low_critical": "Empresas corruptas burlam critérios e obtêm a certificação."}
    ),
    Action(
        action_type="attack", alignment="good", title="Varredura Antidesinformação",
        description="Identifica e neutraliza redes coordenadas de notícias falsas com perícia digital.",
        risk_level="low",
        responses={"high_critical": "Asfixia a capacidade de manipulação digital de extremistas.", "normal_success": "Purifica o debate público de conteúdos fabricados.", "normal_fail": "Redes criminosas migram para plataformas criptografadas.", "low_critical": "A ação é tachada de censura por opositores espertos."}
    ),
    Action(
        action_type="attack", alignment="good", title="Projeto de Lei de Iniciativa Coletiva",
        description="Redige propostas legislativas diretamente com universidades e o povo organizado.",
        risk_level="medium",
        responses={"high_critical": "Aprova leis consistentes e alinhadas ao interesse público real.", "normal_success": "Qualifica o debate legislativo com embasamento técnico.", "normal_fail": "Parlamentares tradicionais barram o avanço nas comissões.", "low_critical": "O texto final é desfigurado por emendas corruptas na calada da noite."}
    )



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