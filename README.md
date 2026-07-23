Foi utilizada a plataforma Docker para padronização do ambiente de desenvolvimento. Permitindo que qualquer integrante da equipe execute o sistema com um único comando (docker compose up --build), sem a necessidade de instalar manualmente Python, Node.js, Redis ou demais dependências do projeto. Caso tenha parado a aplicação, para rodar novamente basta dar "docker compose up". OBS: Para esses comandos darem certo é necessario ter o Docker Desktop aberto.

Para rodar corretamente uma partida demo, além dos passos acima é necessário rodar os seguintes comandos no terminal da raiz do projeto enquanto o docker estiver rodando:
docker compose exec api python -m backend.app.scripts.create_db
docker compose exec api python -m backend.app.scripts.seed_territories
docker compose exec api python -m backend.app.scripts.seed_parties
docker compose exec api python -m backend.app.scripts.seed_missions
docker compose exec api python -m backend.app.scripts.create_demo_match
Assim, terá a primeira partida fake de id 1.

<Arquivo de Versionamento do código
 Enzo - 16/06 | 19:19
 Começo da correção da lógica de ação:
    * Criação da estrutura lógica de quando o round precisar de pergunta.
    * Criação da estrutura lógica de resolução pós possível pergunta.
    * Criação da estrutura lógica de resolução sem pergunta.
    * Definição do passo a passo da ação:
        * Verifica pergunta:
            *Caso tenha
                * Faz pergunta
                * Resolução Pós pergunta 
            *Rolar dado
            *Resolução da ação 
                * Executa a ação correspondente e atribui os atributos corretos
            * Verifica caso algum jogador venceu
                * Caso venceu:
                    * Vitória para o jogador e termina o jogo
                * Caso não:
                    * Próximo round
