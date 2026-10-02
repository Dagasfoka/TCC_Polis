# Perguntas convertidas do arquivo fornecido; bancas e gabaritos não verificados.
from sqlalchemy import delete

from backend.app.db.base import Base
from backend.app.db.database import SessionLocal, engine
from backend.app.models.db.question import Question

QUESTIONS = [
    {
        "subject": "Philosophy",
        "description": "No dia 1º de abril de 1964 aconteceu o golpe militar. O regime político nascido do golpe cometeu diversos crimes contra os direitos humanos. Sobre os Direitos Humanos, é correto afirmar que se fundamentam filosoficamente na consciência social de uma época, segundo a opinião da maioria das pessoas?",
        "exam_board": "UECE-CEV 2024 - Adaptado",
        "options": {
            "A": "Verdadeiro",
            "B": "Falso"
        },
        "answer": "B",
        "difficulty": "easy",
        "explanation": "Na verdade se fundamentam filosoficamente no direito natural e são reconhecidos pela razão, independente das opiniões ou das leis. Mesmo que o Estado viole direitos, eles continuam existindo, dessa forma, permite criticar governos injustos com base em princípios além da lei."
    },
    {
        "subject": "Philosophy",
        "description": "Sobre os conceitos de ética, moral e cidadania, assinale a alternativa correta:",
        "exam_board": "CETREDE - Prefeitura de Maracanaú - 2026 - Adaptado",
        "options": {
            "A": "A ética busca princípios universais de convivência, enquanto a moral varia conforme a cultura e o contexto histórico.",
            "B": "A cidadania está restrita apenas à participação eleitoral em sistemas democráticos."
        },
        "answer": "A",
        "difficulty": "easy",
        "explanation": "A ética reflete princípios gerais sobre o agir humano; a moral corresponde aos costumes e valores específicos de cada sociedade."
    },
    {
        "subject": "Philosophy",
        "description": "Hobbes parte do estado de natureza, no qual não existiria lei, o homem é o lobo do próprio homem; e pelo fato de o homem ser antissocial por natureza, só se torna possível ele viver em sociedade com um Estado extremamente forte. Já Locke diz que o homem não é um ser rebelde à vida política. No estado de natureza, mesmo com ausência de Estado, mesmo com ausência de leis, existe uma vida econômica que torna possível a integração dos indivíduos entre si. Então o Estado nasce para complementar, para tornar possível essa sociabilidade originária, que é a sociabilidade de mercado.\"\nEssas duas concepções políticas são:",
        "exam_board": "UECE-CEV - 2022 - Adaptado",
        "options": {
            "A": "Absolutista, a primeira, e liberal, a segunda.",
            "B": "Liberal, a primeira, e absolutista, a segunda."
        },
        "answer": "A",
        "difficulty": "easy",
        "explanation": "Hobbes defendia um Estado forte para conter o caos; Locke defendia um governo limitado e liberal."
    },
    {
        "subject": "Philosophy",
        "description": "Foi um dos mais importantes filósofos gregos, destacou-se no estudo da ética e foi professor de Platão.",
        "exam_board": "FAU - 2026 - Adaptado",
        "options": {
            "A": "Sócrates",
            "B": "Aristóteles"
        },
        "answer": "A",
        "difficulty": "easy",
        "explanation": "Sócrates foi mestre de Platão e marcou a filosofia pelo foco na ética e no autoconhecimento."
    },
    {
        "subject": "Philosophy",
        "description": "Segundo Platão, a melhor vida é aquela governada pela razão e voltada para a contemplação da verdade. Com base nisso, é correto afirmar que Platão:",
        "exam_board": "UECE-CEV - 2025 - Adaptado",
        "options": {
            "A": "Entende a razão como caminho para a vida justa e feliz.",
            "B": "Considera que paixões e desejos devem governar igualmente a vida humana."
        },
        "answer": "A",
        "difficulty": "easy",
        "explanation": "Para Platão, a razão deve orientar a alma humana, conduzindo o indivíduo à justiça, à verdade e à felicidade."
    },
    {
        "subject": "Philosophy",
        "description": "\"encontrar uma forma de associação que defenda e proteja a pessoa e os bens de cada associado com toda a força comum, e pela qual cada um, unindo-se a todos, só obedece contudo a si mesmo, permanecendo assim tão livre como antes. Esse é o problema fundamental cuja solução o contrato social oferece\"Quem propôs essa ideia de contrato social?",
        "exam_board": "UEG - 2024 - Adaptado",
        "options": {
            "A": "Jean-Jacques Rousseau",
            "B": "John Locke"
        },
        "answer": "A",
        "difficulty": "medium",
        "explanation": "Rousseau defendia que o indivíduo continua livre ao obedecer à vontade geral construída coletivamente."
    },
    {
        "subject": "Philosophy",
        "description": "\"Mary Wollstonecraft abre sua obra, Reivindicações dos direitos da mulher (1792), com uma carta ao Sr. Talleyrand-Périgord. Nesta carta, Wollstonecraft afirma:\n\n\"Mas, se as mulheres devem ser excluídas, sem voz, da participação dos direitos naturais da humanidade, prove antes, para afastar a acusação de injustiça e inconsistência, que elas são desprovidas de razão; de outro modo, essa falha em sua NOVA CONSTITUIÇÃO sempre mostrará que o homem deve de alguma forma agir como um tirano, e a tirania, quando mostra sua face despudorada em qualquer parte da sociedade, sempre solapa a moralidade.\" Segundo Mary Wollstonecraft, excluir mulheres dos direitos políticos é injusto porque:",
        "exam_board": "COMVEST - UNICAMP - 2024 - Adaptado",
        "options": {
            "A": "A participação política feminina deve ocorrer quando houver igualdade moral entre homens e mulheres.",
            "B": "Não existe prova de inferioridade racional das mulheres."
        },
        "answer": "B",
        "difficulty": "medium",
        "explanation": "Se mulheres são racionais, devem ter direitos; caso contrário, prove que não são. Essa é a linha de raciocínio de Wollstonecraft"
    },
    {
        "subject": "Philosophy",
        "description": "Ao relacionar a Alegoria da Caverna, de Platão, aos dias atuais, é possível:",
        "exam_board": "Adaptado",
        "options": {
            "A": "Questionar o senso comum e as opiniões presentes nas redes sociais.",
            "B": "Constatar como as redes sociais se aproximam do mundo das ideias."
        },
        "answer": "A",
        "difficulty": "medium",
        "explanation": "A Alegoria da Caverna critica percepções ilusórias e o apego às aparências, algo associado ao senso comum e às redes sociais."
    },
    {
        "subject": "Philosophy",
        "description": "Sobre as origens da filosofia e sua relação com o mito, assinale a alternativa correta:",
        "exam_board": "UNICENTRO - 2025",
        "options": {
            "A": "A filosofia surge da busca racional pela compreensão da physis e da origem do cosmos.",
            "B": "A filosofia nasceu em Atenas no século IV a.C. como continuação do pensamento estoico."
        },
        "answer": "A",
        "difficulty": "medium",
        "explanation": "Os pré-socráticos buscavam explicar racionalmente a natureza e a origem do mundo. A physis representa a natureza e o princípio fundamental de tudo o que existe."
    },
    {
        "subject": "Philosophy",
        "description": "Existe uma teoria ética que defende a busca do máximo de felicidade para o maior número possível de pessoas, mesmo que isso exija sacrifícios individuais. Essa teoria é chamada de:",
        "exam_board": "SELECON - EMGEPRON - 2026 - Adaptado",
        "options": {
            "A": "Utilitarismo",
            "B": "Comunismo"
        },
        "answer": "A",
        "difficulty": "medium",
        "explanation": "O utilitarismo avalia as ações pelos seus resultados, buscando o maior bem-estar coletivo possível."
    },
    {
        "subject": "Philosophy",
        "description": "Segundo Jean-Jacques Rousseau, os avanços das sociedades humanas produziram efeitos negativos sobre o ser humano. Com base nisso, é correto afirmar que Rousseau defendia que:",
        "exam_board": "FUNDATEC - IFC-SC - 2026 - Adaptado",
        "options": {
            "A": "Os progressos das sociedades contribuíram para a deterioração moral e para a desigualdade humana.",
            "B": "A indústria e a agricultura têm a função de aprimorar a humanidade coletivamente."
        },
        "answer": "A",
        "difficulty": "hard",
        "explanation": "Rousseau entendia que a civilização e a propriedade privada corromperam a bondade natural humana."
    },
    {
        "subject": "Sociology",
        "description": "Sobre o racismo estrutural e a naturalização de expressões racistas no cotidiano, assinale a alternativa INCORRETA:",
        "exam_board": "IESES - 2022 - Prefeitura de Biguaçu - SC - Adaptado",
        "options": {
            "A": "A discussão de uma educação antirracista inclui a conscientização sobre o uso de vocabulário racista e seus impactos sociais.",
            "B": "É importante mencionar o equívoco desse vocabulário, mas sem grande ênfase, para evitar possíveis efeitos reversos."
        },
        "answer": "B",
        "difficulty": "medium",
        "explanation": "A educação antirracista envolve problematizar e combater expressões discriminatórias de forma crítica e contínua. Minimizar essa discussão pode contribuir para a manutenção do racismo estrutural."
    },
    {
        "subject": "Sociology",
        "description": "A mobilização social é um instrumento de fortalecimento da cidadania e de construção coletiva de direitos sociais. Assinale a alternativa correta:",
        "exam_board": "UNIDAVI - 2026 - Prefeitura de Agrolândia - SC - Adaptado",
        "options": {
            "A": "Consiste em processo coletivo que busca engajamento social para transformação da realidade e fortalecimento democrático.",
            "B": "Possui caráter apenas informativo, sem impacto nas decisões públicas."
        },
        "answer": "A",
        "difficulty": "easy",
        "explanation": "A mobilização social envolve participação coletiva e engajamento político, contribuindo para a transformação social e fortalecimento da democracia. Não se limita à informação nem substitui instituições formais."
    },
    {
        "subject": "Sociology",
        "description": "Para Bauman, nas sociedades capitalistas e consumistas contemporâneas, viver a crédito cria tanta dependência como um vício em drogas. Atualmente existe todo tipo de influência mercadológica e de acesso a crédito facilitado. Para este autor,ingressar hoje na condição de consumidor endividado está mais fácil do que nunca antes na história da humanidade, mas escapar dessa condição jamais foi tão difícil. Com base na análise de Zygmunt Bauman sobre o consumismo contemporâneo e o endividamento dos consumidores, assinale a alternativa correta:",
        "exam_board": "UECE-CEV - 2025 - UECE - Adaptado",
        "options": {
            "A": "O capitalismo contemporâneo se sustenta também pela lógica do endividamento dos consumidores, que se torna fonte contínua de lucro para o sistema financeiro.",
            "B": "O principal problema do endividamento é a ausência de cursos de educação financeira oferecidos pelo Estado."
        },
        "answer": "A",
        "difficulty": "easy",
        "explanation": "Bauman aponta que o consumo a crédito é estrutural no capitalismo contemporâneo, funcionando como mecanismo de lucro contínuo. Não se trata apenas de falta de educação financeira, mas de uma dinâmica sistêmica que incentiva o endividamento."
    },
    {
        "subject": "Sociology",
        "description": "O ser humano desenvolveu diferentes formas de trabalho ao longo da história, como o trabalho escravo, servil e assalariado. Com base nesse conhecimento,  sintetizado a partir das contribuições de Karl Marx, identifique a dimensão do trabalho abordada.",
        "exam_board": "FUNCERN - 2024 - Adaptado",
        "options": {
            "A": "Dimensão histórica, relacionada às transformações das formas de trabalho ao longo do tempo.",
            "B": "Dimensão gnosiológica do trabalho, relacionada à teoria do conhecimento sobre o trabalho."
        },
        "answer": "A",
        "difficulty": "medium",
        "explanation": "O fragmento trata da evolução das formas de trabalho ao longo do tempo (escravo, servil e assalariado). Isso caracteriza a dimensão histórica do trabalho em Marx."
    },
    {
        "subject": "Sociology",
        "description": "Sobre o movimento surdo, que surgiu a partir das reivindicações por reconhecimento cultural e linguístico das pessoas surdas, assinale a alternativa INCORRETA:",
        "exam_board": "FUNDATEC - 2026 - IFC-SC - Adaptado",
        "options": {
            "A": "O movimento surdo contribuiu para superar interpretações exclusivamente clínicas da surdez, mas manteve como referência predominante a ideia de deficiência.",
            "B": "O movimento surdo defende o reconhecimento da língua de sinais e da cultura surda como elementos centrais de sua identidade coletiva."
        },
        "answer": "A",
        "difficulty": "medium",
        "explanation": "O movimento surdo rompe com a visão predominante da surdez como deficiência e a compreende como uma identidade cultural e linguística própria."
    },
    {
        "subject": "Sociology",
        "description": "Sobre desigualdades sociais, educação e mobilidade social, assinale a alternativa correta:",
        "exam_board": "FADESP - 2020 - UEPA - Adaptado",
        "options": {
            "A": "A renda e o status social são estatisticamente dependentes da origem social e do nível de instrução, de forma moderada.",
            "B": "A origem social determina as condições de desigualdade das famílias, impossibilitando a mobilidade social."
        },
        "answer": "A",
        "difficulty": "medium",
        "explanation": "A origem social e a escolaridade influenciam as oportunidades dos indivíduos, mas não impedem completamente a mobilidade social."
    },
    {
        "subject": "Sociology",
        "description": "Ao afirmar que o Estado Moderno detém o monopólio da força legítima, Max Weber buscava descrever:",
        "exam_board": "FADESP - 2020 - UEPA - Adaptado",
        "options": {
            "A": "O monopólio da força como um atributo político das autoridades consideradas legítimas.",
            "B": "A legitimação da violência como forma de coerção social aceita por todos quando exercida em nome do Estado."
        },
        "answer": "A",
        "difficulty": "medium",
        "explanation": "Para Weber, o Estado é a instituição que reivindica com êxito o uso legítimo da força em determinado território. Isso não significa que todos aceitem essa violência, mas que ela é socialmente reconhecida como legítima."
    },
    {
        "subject": "Sociology",
        "description": "Considerando a concepção de Max Weber sobre a ciência como parte do processo de racionalização das sociedades modernas, assinale a alternativa correta:",
        "exam_board": "IF-RR - 2015",
        "options": {
            "A": "A ciência, como parte do processo histórico de racionalização, caracteriza-se pela busca da objetividade e pelo caráter não definitivo do conhecimento científico.",
            "B": "A ciência é um processo definitivo, orientado pelos juízos de valor do cientista."
        },
        "answer": "A",
        "difficulty": "hard",
        "explanation": "Para Weber, a ciência deve buscar objetividade e neutralidade valorativa, produzindo conhecimentos sempre provisórios e passíveis de revisão."
    },
    {
        "subject": "Sociology",
        "description": "Para Auguste Comte, diante das transformações provocadas pela sociedade industrial no século XIX, assinale a alternativa correta:",
        "exam_board": "IF-RR - 2015",
        "options": {
            "A": "A oposição entre empresários e operários era secundária, resultante da desorganização da sociedade industrial e passível de correção por meio de reformas.",
            "B": "A sociedade deveria ser explicada pelo estado metafísico, considerado por Comte a etapa mais avançada do conhecimento humano."
        },
        "answer": "A",
        "difficulty": "hard",
        "explanation": "Comte entendia os conflitos sociais como consequências transitórias da desordem provocada pelas mudanças industriais. Para ele, a reorganização científica da sociedade restauraria a ordem. Já o estado positivo, e não o metafísico, representa o estágio mais avançado do conhecimento."
    },
    {
        "subject": "Sociology",
        "description": "Em Durkheim, o princípio de integração sustenta a concepção de solidariedade e permite classificar o fato social como patológico ou anômico.",
        "exam_board": "CESPE - 2004 - Adaptado",
        "options": {
            "A": "Certo",
            "B": "Errado"
        },
        "answer": "A",
        "difficulty": "medium",
        "explanation": "Em Durkheim, a integração social está ligada ao grau de coesão da sociedade e à solidariedade. A ausência ou falha dessa integração pode levar a estados de anomia ou patologia social. Por isso, a afirmação está correta dentro do referencial durkheimiano."
    },
    {
        "subject": "Philosophy",
        "description": "Karl Marx desenvolveu o conceito de 'fetiche da mercadoria' para explicar como as relações sociais no capitalismo aparecem de forma distorcida. Assinale a alternativa correta:",
        "exam_board": "FUNDATEC - 2026 - IFC-SC - Adaptado",
        "options": {
            "A": "O valor das mercadorias é dado pela relação entre as pessoas e seus trabalhos.",
            "B": "O valor das mercadorias é dado pela relação entre coisas como produtos autônomos."
        },
        "answer": "B",
        "difficulty": "hard",
        "explanation": "No fetichismo da mercadoria, as relações entre trabalhadores aparecem como relações entre coisas, ocultando a origem social do valor."
    },
    {
        "subject": "Sociology",
        "description": "Segundo Max Weber, a dominação carismática baseia-se na crença das qualidades extraordinárias de um líder. Considerando as afirmações apresentadas, assinale a alternativa correta:",
        "exam_board": "IF-PI - 2026 - IF-PI - Adaptado",
        "options": {
            "A": "A teoria de dominação carismática representa a possibilidade, no sistema teórico weberiano, de rompimento efetivo, apesar de temporário, das outras formas de dominação.",
            "B": "Na teoria de dominação carismática, a legitimidade se estabelece através da crença na legalidade das normas estatuídas e dos direitos de mando dos que exercem a autoridade."
        },
        "answer": "A",
        "difficulty": "hard",
        "explanation": "A dominação carismática ocorre quando os seguidores obedecem a um líder devido à devoção pessoal e à crença em suas qualidades excepcionais, heroicas e não por tradições ou regras burocráticas. É uma forma de autoridade de caráter instável, pois depende diretamente da figura do líder, podendo se alterar ou desaparecer com sua ausência."
    },
    {
        "subject": "Sociology",
        "description": "Segundo Max Weber, a ética protestante teve papel importante no desenvolvimento do capitalismo moderno. Assinale a alternativa correta:",
        "exam_board": "IF-PA - 2022 - Adaptado",
        "options": {
            "A": "A ética protestante fez do trabalho um valor em si mesmo, associado à disciplina e ao desenvolvimento espiritual do indivíduo.",
            "B": "O protestantismo defendia a acumulação de riqueza e sua ostentação como demonstração pública de salvação."
        },
        "answer": "A",
        "difficulty": "hard",
        "explanation": "Para Weber, a ética protestante valorizava o trabalho disciplinado e a ascese. A riqueza podia ser acumulada, mas não deveria ser ostentada."
    },
    {
        "subject": "History",
        "description": "O Movimento Bandeirante teve um papel importante na história de São Paulo e do Brasil. Qual era seu principal objetivo inicial?",
        "exam_board": "Adaptado",
        "options": {
            "A": "Desbravar o interior em busca de metais preciosos.",
            "B": "Instalação de indústrias automobilísticas"
        },
        "answer": "A",
        "difficulty": "easy",
        "explanation": "Os bandeirantes exploravam o interior do território em busca de riquezas minerais e captura de indígenas."
    },
    {
        "subject": "History",
        "description": "A respeito da Era Vargas e da implantação da ditadura militar no Brasil, assinale a alternativa correta.",
        "exam_board": "MPE-GO - 2026 - Adaptado",
        "options": {
            "A": "O Estado Novo manteve o pluripartidarismo e ampliou a autonomia dos estados, enquanto o regime militar instaurado em 1964 fortaleceu a participação popular direta nas decisões nacionais.",
            "B": "Tanto o Estado Novo quanto a ditadura militar caracterizaram-se pela centralização do poder, restrição de liberdades e repressão política."
        },
        "answer": "B",
        "difficulty": "easy",
        "explanation": "Ambos foram regimes autoritários com centralização do poder e repressão política."
    },
    {
        "subject": "History",
        "description": "A Revolução de 1930 foi um movimento armado que resultou no fim da política do café com leite e na ascensão de Getúlio Vargas ao poder. Sobre as causas e o contexto desse evento, assinale a alternativa correta:",
        "exam_board": "MPE-GO - 2026 - Adaptado",
        "options": {
            "A": "A Revolução foi motivada exclusivamente pela crise econômica de 1929, sem influência de disputas políticas internas entre as oligarquias.",
            "B": "O rompimento do acordo entre as oligarquias ocorreu quando Washington Luís indicou o paulista Júlio Prestes como seu sucessor."
        },
        "answer": "B",
        "difficulty": "easy",
        "explanation": "O rompimento do acordo entre São Paulo e Minas Gerais ocorreu com a indicação de Júlio Prestes, quebrando a lógica da política do café com leite."
    },
    {
        "subject": "History",
        "description": "O Dia da Consciência Negra, celebrado em 20 de novembro, foi instituído no Brasil em memória de qual fato histórico?",
        "exam_board": "UNIOESTE - 2026 - Câmara de São Miguel do Iguaçu - PR - Adaptado",
        "options": {
            "A": "A morte de Zumbi dos Palmares, líder da resistência contra a escravidão.",
            "B": "A assinatura da Lei Áurea pela Princesa Isabel, que aboliu a escravidão."
        },
        "answer": "A",
        "difficulty": "easy",
        "explanation": "A data homenageia Zumbi dos Palmares, símbolo da resistência à escravidão no Brasil."
    },
    {
        "subject": "History",
        "description": "A primeira atividade de exploração florestal no Brasil, durante o período colonial, esteve relacionada principalmente à:",
        "exam_board": "FUVEST - 2026 - USP - Adaptado",
        "options": {
            "A": "Mineração do ouro.",
            "B": "Exploração do pau-brasil."
        },
        "answer": "B",
        "difficulty": "easy",
        "explanation": "A primeira atividade econômica de exploração florestal no Brasil foi o pau-brasil, usado principalmente para extração de corante vermelho."
    },
    {
        "subject": "History",
        "description": "A mudança na forma como os senhores tratavam os escravizados após 1830 e 1850 foi provocada principalmente por:",
        "exam_board": "VUNESP - 2025 - UNIFIPA - Adaptado",
        "options": {
            "A": "Pelas ações de estímulo à imigração de europeus, que proporcionaram o ingresso no país de mão de obra especializada e mais adequada ao trabalho.",
            "B": "Leis que proibiram o tráfico de escravizados, elevando seu valor no mercado."
        },
        "answer": "B",
        "difficulty": "easy",
        "explanation": "Com a proibição do tráfico negreiro, os escravizados passaram a ter maior valor econômico, reduzindo sua substituição."
    },
    {
        "subject": "History",
        "description": "Durante o início do século XX, no contexto da colonização e da construção da Estrada de Ferro São Paulo–Rio Grande, qual conflito ocorreu na região e a transformou em um grande campo de batalha?",
        "exam_board": "FUNDATEC - 2026 - Prefeitura de Pinheiro Preto - SC - Adaptado",
        "options": {
            "A": "Guerra de Canudos.",
            "B": "Guerra do Contestado."
        },
        "answer": "B",
        "difficulty": "medium",
        "explanation": "A Guerra do Contestado ocorreu entre 1912 e 1916 na região Sul do Brasil, envolvendo conflitos por terra entre posseiros, trabalhadores e o Estado, além da atuação de empresas ferroviárias e madeireiras. O conflito surgiu a partir da desapropriação de terras e da expulsão de populações locais durante obras de infraestrutura, como a construção da Estrada de Ferro São Paulo–Rio Grande, resultando em forte resistência contra o governo."
    },
    {
        "subject": "History",
        "description": "Na democracia ateniense de 451 a.C., a participação política era caracterizada por:",
        "exam_board": "VUNESP - 2025 - UNIFIPA - Adaptado",
        "options": {
            "A": "A democracia era representativa e contava com membros de todos os setores sociais.",
            "B": "Participação política plena de todos os grupos sociais da cidade."
        },
        "answer": "A",
        "difficulty": "medium",
        "explanation": "Na democracia ateniense, indivíduos do sexo feminino, escravizados e estrangeiros eram excluídos da cidadania."
    },
    {
        "subject": "History",
        "description": "Os impulsos democráticos ocorridos em países africanos no final dos anos 1980 e início dos anos 1990 associam-se principalmente:",
        "exam_board": "VUNESP - 2025 - UNIFIPA - Adaptado",
        "options": {
            "A": "À combinação de mobilizações internas com mudanças no cenário internacional.",
            "B": "Ao surgimento dos processos de descolonização nas regiões centrais da África."
        },
        "answer": "A",
        "difficulty": "medium",
        "explanation": "A redemocratização africana foi influenciada tanto por pressões internas quanto pelo fim da Guerra Fria e da União Soviética."
    },
    {
        "subject": "History",
        "description": "Sobre o Plano de Metas do governo Juscelino Kubitschek, assinale a alternativa correta:",
        "exam_board": "FGV - 2025 - FEMPAR - Adaptado",
        "options": {
            "A": "O governo priorizou a ampliação das rodovias e a integração territorial do país.",
            "B": "Incentivo à mecanização da agricultura para modernizar a infraestrutura do setor e aumentar a eficiência produtiva."
        },
        "answer": "B",
        "difficulty": "medium",
        "explanation": "O governo JK buscou acelerar a mecanização da agricultura  e modernizar a economia brasileira por meio do desenvolvimentismo."
    },
    {
        "subject": "History",
        "description": "O Estado Novo varguista (1937-1945) e a ditadura militar (1964-1985) apresentam similitudes e contraposições. Acerca desses períodos históricos, assinale a alternativa correta:",
        "exam_board": "IBEST - 2025 - UCB - Adaptado",
        "options": {
            "A": "Similitudes emergem nos modelos econômicos e políticos desses dois períodos: ambos eram nacionalistas, defendiam a forte presença do Estado em todas as áreas da economia e repudiavam a presença de investimentos estrangeiros.",
            "B": "Os meios de propaganda no Estado Novo foram utilizados de tal maneira que, para a consolidação do poder, a imagem personalista de Getúlio Vargas como líder e realizador."
        },
        "answer": "B",
        "difficulty": "hard",
        "explanation": "Durante o Estado Novo, o DIP estruturou uma propaganda estatal que exaltava Vargas, censurava críticas e legitimava o regime autoritário. Esse padrão de controle informacional também se manifesta na ditadura militar por meio da censura e da comunicação oficial centralizada."
    },
    {
        "subject": "Geography",
        "description": "Assinale a alternativa que apresenta a melhor descrição da chamada zona de subducção.",
        "exam_board": "FUVEST - 2025 - USP - Adaptado",
        "options": {
            "A": "Região caracterizada pela colisão entre duas placas tectônicas, sendo que uma é empurrada para baixo da outra.",
            "B": "Região na qual as placas tectônicas se afastam umas das outras."
        },
        "answer": "A",
        "difficulty": "easy",
        "explanation": "A subducção ocorre quando uma placa tectônica mergulha sob outra em uma zona de convergência."
    },
    {
        "subject": "Geography",
        "description": "É correto afirmar que as placas tectônicas são:",
        "exam_board": "FUVEST - 2025 - USP - Adaptado",
        "options": {
            "A": "Camadas sucessivas de rochas que formam o núcleo terrestre.",
            "B": "Fragmentos da crosta e da parte superior do manto terrestre."
        },
        "answer": "B",
        "difficulty": "easy",
        "explanation": "As placas tectônicas são blocos rígidos formados pela crosta e pela porção superior do manto, que se movimentam sobre a astenosfera."
    },
    {
        "subject": "Geography",
        "description": "Assinale o tipo climático predominante na região do Brasil que apresenta pela maior frequência de episódios de neve",
        "exam_board": "FGV - 2026 - IBGE - Adaptado",
        "options": {
            "A": "Subtropical.",
            "B": "Equatorial."
        },
        "answer": "A",
        "difficulty": "easy",
        "explanation": "O Sul do Brasil possui clima subtropical, com temperaturas mais baixas em relação ao trópico e ocorrência ocasional de neve nas áreas de maior altitude."
    },
    {
        "subject": "Geography",
        "description": "Entre 2010 e 2022, a população brasileira apresentou envelhecimento demográfico, com redução da natalidade e crescimento da população idosa. Considerando esse cenário, verifica-se uma tendência à:",
        "exam_board": "FGV - 2026 - IBGE",
        "options": {
            "A": "Intensificação da pressão sobre a Previdência Social e aumento dos gastos com saúde voltados à população idosa.",
            "B": "Ampliação prioritária dos investimentos na Educação Básica devido ao crescimento da população infantil."
        },
        "answer": "A",
        "difficulty": "easy",
        "explanation": "O envelhecimento populacional aumenta a demanda por aposentadorias e serviços de saúde destinados aos idosos."
    },
    {
        "subject": "Geography",
        "description": "A tecnologia de geolocalização utilizada em dispositivos móveis para identificar a posição de pessoas ou objetos na superfície terrestre baseia-se em:",
        "exam_board": "FGV - 2026 - IBGE - Adaptado",
        "options": {
            "A": "Fusos horários.",
            "B": "Coordenadas geográficas."
        },
        "answer": "B",
        "difficulty": "easy",
        "explanation": "A geolocalização funciona a partir de coordenadas geográficas (latitude e longitude), que permitem localizar pontos na superfície terrestre."
    },
    {
        "subject": "Geography",
        "description": "A partir da regionalização do território brasileiro adotada pelo IBGE, relacione corretamente cada estado à sua respectiva Grande Região.\n\n1. Ceará\n2. Tocantins\n3. Mato Grosso\n\n(   ) Norte\n(   ) Nordeste\n(   ) Centro-Oeste",
        "exam_board": "FGV - 2026 - IBGE - Adaptado",
        "options": {
            "A": "2 – 1 – 3",
            "B": "1 – 2 – 3"
        },
        "answer": "A",
        "difficulty": "easy",
        "explanation": "Tocantins pertence ao Norte, Ceará ao Nordeste e Mato Grosso ao Centro-Oeste."
    },
    {
        "subject": "Geography",
        "description": "A urbanização brasileira consolidou-se de forma acelerada ao longo do século XX, resultando em reorganização do espaço urbano e desigualdades socioespaciais. Considerando esse contexto, assinale a alternativa correta:",
        "exam_board": "CEV-URCA - 2026 - Prefeitura de Assaré - CE - Adaptado",
        "options": {
            "A": "A metropolização brasileira promoveu a desconcentração de renda e a distribuição de infraestrutura urbana entre centro e periferia;",
            "B": "A segregação socioespacial nas cidades brasileiras manifesta-se na valorização de áreas com infraestrutura e na marginalização de populações de baixa renda em periferias ou áreas vulneráveis."
        },
        "answer": "B",
        "difficulty": "easy",
        "explanation": "A urbanização brasileira gerou forte desigualdade socioespacial, com valorização de áreas centrais e exclusão de populações pobres para periferias e regiões menos estruturadas."
    },
    {
        "subject": "Geography",
        "description": "Sobre o Estreito de Ormuz e sua importância geoeconômica, assinale a alternativa correta:",
        "exam_board": "IBEPP - 2026 - Prefeitura de Tupã - SP - Adaptado",
        "options": {
            "A": "O Estreito de Ormuz é uma rota estratégica para o escoamento de petróleo do Golfo Pérsico.",
            "B": "O Estreito de Ormuz conecta diretamente o Mar Mediterrâneo ao Oceano Índico."
        },
        "answer": "A",
        "difficulty": "medium",
        "explanation": "O Estreito de Ormuz é uma das principais rotas do comércio mundial de petróleo, ligando o Golfo Pérsico ao Oceano Índico."
    },
    {
        "subject": "Geography",
        "description": "Sobre a reforma agrária e a reestruturação fundiária no Brasil, assinale a alternativa correta:",
        "exam_board": "FGV - 2026 - IBGE - Adaptado",
        "options": {
            "A": "A reforma agrária pode reduzir conflitos no campo e fortalecer a agricultura familiar, gerando emprego no meio rural e aumentando a produção de alimentos.",
            "B": "A reforma agrária consiste na expropriação e doação de terras privadas pelo governo, promovendo sua função social ."
        },
        "answer": "A",
        "difficulty": "medium",
        "explanation": "A reforma agrária busca democratizar o acesso à terra, reduzir desigualdades no campo e estimular a agricultura familiar, o que tende a diminuir conflitos fundiários e ampliar a produção de alimentos. \"A alternativa B está incorreta porque reduz a reforma agrária a uma simples expropriação e doação de terras"
    },
    {
        "subject": "Geography",
        "description": "Sobre a definição de região metropolitana, avalie os itens a seguir:\n\nI. Possui uma conectividade intensa entre os municípios.\n\nII. Apresenta uma cidade principal, que concentra a maior oferta de empregos/serviços à população.\nIII. Enfrenta problemas e demandas comuns aos municípios que a compõem, o que exige gestão integrada e coordenação entre os governos municipais.",
        "exam_board": "FGV - 2026 - IBGE - Adaptado",
        "options": {
            "A": "I, II e III.",
            "B": "I e III, apenas."
        },
        "answer": "A",
        "difficulty": "easy",
        "explanation": "Todas as afirmativas estão corretas: regiões metropolitanas possuem forte integração entre municípios, centralização de serviços na metrópole e gestão conjunta de problemas comuns."
    },
    {
        "subject": "Geography",
        "description": "A recarga de aquíferos livres ocorre geralmente de forma mais intensa em regiões com:",
        "exam_board": "FGV - 2025 - CPRM - Adaptado",
        "options": {
            "A": "Declividades acentuadas.",
            "B": "Solos arenosos com alta permeabilidade."
        },
        "answer": "B",
        "difficulty": "medium",
        "explanation": "A recarga é maior em solos arenosos porque a alta permeabilidade facilita a infiltração da água. A declividade acentuada favorece o escoamento superficial da água, fazendo com que ela escoe rapidamente sem infiltrar no solo."
    },
    {
        "subject": "Geography",
        "description": "Os fluxos migratórios contemporâneos configuram-se como fenômenos complexos, relacionados a fatores econômicos, políticos, ambientais e culturais. Considerando esse contexto, assinale a alternativa correta:",
        "exam_board": "IGEDUC - 2026 - Prefeitura de Pão de Açúcar - AL - Adaptado",
        "options": {
            "A": "A migração pendular caracteriza-se por deslocamentos definitivos entre países distintos, com mudança permanente de residência e nacionalidade jurídica.",
            "B": "O êxodo rural pode provocar crescimento acelerado das cidades, pressionando infraestrutura urbana e ampliando desigualdades socioespaciais."
        },
        "answer": "B",
        "difficulty": "medium",
        "explanation": "O êxodo rural intensifica a urbanização desordenada, gerando pressão sobre infraestrutura urbana e ampliando desigualdades socioespaciais."
    },
    {
        "subject": "Geography",
        "description": "O ecossistema costeiro constitui uma zona de transição entre sistemas continentais e oceânicos. Considerando o uso racional do mar e a organização socioambiental das zonas costeiras, assinale a alternativa correta:",
        "exam_board": "IDECAN - 2026 - Prefeitura de Feira de Santana - BA - Adaptado",
        "options": {
            "A": "O manejo costeiro integrado pressupõe articulação entre processos naturais, atividades econômicas e ordenamento territorial, reconhecendo a interdependência entre ambientes marinhos, costeiros e continentais.",
            "B": "A conservação dos ecossistemas costeiros depende da segregação espacial entre áreas naturais e áreas produtivas, reduzindo a necessidade de instrumentos de gestão integrada."
        },
        "answer": "A",
        "difficulty": "hard",
        "explanation": "O manejo integrado das zonas costeiras considera a interação entre meio físico e atividades humanas, exigindo planejamento conjunto e gestão territorial articulada."
    }
]

def seed_questions():
    Base.metadata.create_all(bind=engine)

    with SessionLocal.begin() as db:
        db.execute(delete(Question))
        db.add_all([Question(**data) for data in QUESTIONS])

    print(f"{len(QUESTIONS)} questões cadastradas.")


if __name__ == "__main__":
    seed_questions()
