Foi utilizada a plataforma Docker para padronização do ambiente de desenvolvimento. Permitindo que qualquer integrante da equipe execute o sistema com um único comando (docker compose up --build), sem a necessidade de instalar manualmente Python, Node.js, Redis ou demais dependências do projeto. Para parar execute o comando docker compose down e para voltar basta digitar docker compose up.
Após os passos acima, para rodar corretamente uma partida demo basta rodas docker compose exec api task demo_match

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
