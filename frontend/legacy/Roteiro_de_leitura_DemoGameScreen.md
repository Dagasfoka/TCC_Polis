# Roteiro de leitura — `DemoGameScreen`

## Explicação geral em uma frase

O `DemoGameScreen` é o componente React que conecta um jogador a uma partida pelo WebSocket, guarda no front-end o estado mais recente enviado pelo backend e transforma esse estado em uma interface interativa.

## O que o componente faz e o que ele não faz

### O que ele faz

- abre e fecha a conexão WebSocket;
- recebe eventos do backend;
- guarda o estado recebido em `matchState`;
- mostra mapa, jogadores, turno, missão e resultados;
- envia escolhas de ataque e respostas de perguntas;
- controla elementos visuais, como território selecionado e modal.

### O que ele não faz

- não calcula o resultado do ataque;
- não decide se o jogador pode agir de verdade;
- não verifica a conclusão da missão;
- não escolhe o vencedor;
- não persiste a partida.

Essas regras pertencem ao backend. O front apenas apresenta os dados e envia as intenções do usuário.

---

## Ordem recomendada de leitura

### 1. Imports e constantes

Primeiro são importados os hooks do React e o componente `BrazilMapSvg`. Depois, `PARTY_COLORS` relaciona cada partido a uma cor usada no mapa e na lista de jogadores.

### 2. Funções auxiliares

- `formatMission`: converte a estrutura JSON da missão em texto legível.
- `summarizeEvent`: diminui eventos grandes antes de mostrá-los no log.
- `getPlayerNameById`: transforma um ID em `nome (id)`.

Essas funções não alteram o estado da partida. Apenas preparam dados para a interface.

### 3. Estados do React

Os principais são:

- `matchId` e `playerId`: dados usados para conectar;
- `connected`: estado visual da conexão;
- `matchState`: cópia mais recente da partida recebida do servidor;
- `selectedTerritory`: território clicado no mapa;
- `logs`: histórico de comunicação;
- `pendingQuestion`: controla a abertura do modal;
- `pendingActionInfo`: informações da ação ligada à pergunta.

A variável mais importante é `matchState`, porque quase toda a interface é desenhada a partir dela.

### 4. Referências com `useRef`

- `wsRef` guarda a conexão WebSocket;
- `winnerAlertShownRef` registra se o alerta de vitória já apareceu.

`useRef` é adequado porque esses valores precisam sobreviver às renderizações, mas suas mudanças não precisam redesenhar a tela.

### 5. Dados derivados

A partir de `matchState`, o componente obtém:

- `players`;
- `territories`;
- `attackOptions`;
- `currentPlayer`;
- `me`;
- `isMyTurn`.

Esses dados não são novos estados independentes. Eles são calculados a partir do estado principal.

### 6. Conexão WebSocket

`connect()`:

1. valida `matchId` e `playerId`;
2. fecha uma conexão anterior;
3. cria a URL do WebSocket;
4. guarda a conexão em `wsRef`;
5. configura os callbacks `onopen`, `onmessage`, `onerror` e `onclose`.

O callback mais importante é `onmessage`, pois todo dado enviado pelo backend entra por ele.

### 7. Tratamento dos eventos recebidos

O `onmessage` aceita alguns formatos:

#### `attack_question`

Guarda a pergunta em `pendingQuestion`, o que faz o modal aparecer.

#### `match_state`

Pega o estado de `data.payload` e atualiza `matchState`.

#### `attack_result` dentro de `data.result`

Pega o novo estado de `data.match`, fecha o modal e atualiza a partida.

#### resposta genérica com `match` e `result`

Aceita outras ações do protótipo que também devolvam o novo estado.

#### `error`

Mostra a mensagem enviada pelo backend.

Os vários formatos indicam uma camada de compatibilidade durante o desenvolvimento. Em uma versão mais consolidada, seria interessante padronizar todos os eventos.

### 8. Envio de uma ação

`sendAttack(optionId)`:

1. confirma que o WebSocket está aberto;
2. confirma que existe um território selecionado;
3. monta o evento `choose_attack_option`;
4. envia o JSON ao backend;
5. registra a ação no log;
6. limpa a seleção do mapa.

O front não aplica influência nem troca o dono do território. Ele espera o backend calcular e devolver o novo estado.

### 9. Resposta da pergunta

`answerAttackQuestion(answer)` envia `true` ou `false` usando o evento `answer_attack_question`.

Após o envio, o modal é fechado. O resultado real só aparece quando o backend responde.

### 10. Limpeza do componente

O `useEffect` retorna uma função que fecha o WebSocket quando a tela é desmontada. Isso evita conexões abandonadas ao trocar de página.

### 11. Renderização JSX

A interface está dividida em:

1. barra de conexão;
2. sidebar com dados da partida;
3. mapa central;
4. painel de logs;
5. modal de pergunta.

Sempre que um estado muda, React executa o componente novamente e atualiza os trechos afetados.

---

## Fluxo completo para explicar na apresentação

> O usuário informa a partida e o jogador. A função `connect` abre um WebSocket com o backend. Quando o backend envia o estado da partida, o evento entra em `onmessage` e é armazenado em `matchState`. A interface é renderizada a partir desse estado. Quando o jogador clica no mapa, o território é guardado em `selectedTerritory`. Ao escolher uma ação, `sendAttack` envia apenas a intenção para o backend. Caso seja necessária uma pergunta, o backend envia `attack_question`, que abre o modal. A resposta é enviada por `answerAttackQuestion`. O backend então calcula o resultado, atualiza a partida e devolve um novo estado, que substitui o `matchState` anterior e atualiza toda a tela.

---

## Conceitos de React que aparecem

### Estado controlado

Os inputs usam `value` e `onChange`. O valor visível vem do estado, e toda digitação atualiza esse estado.

### Renderização condicional

Exemplos:

- `connected ? "Reconectar" : "Conectar"`;
- `selectedTerritory ? (...) : (...)`;
- `pendingQuestion && (...)`.

### Listas com `map`

São usadas para criar:

- botões das opções de ataque;
- lista de jogadores;
- itens do log.

Cada item recebe uma `key` única.

### Comunicação pai-filho

O `DemoGameScreen` passa dados ao `BrazilMapSvg` por props. O mapa devolve a seleção chamando `onSelectTerritory`, que é a própria função `setSelectedTerritory`.

---

## Perguntas que podem fazer

### Por que usar WebSocket e não apenas HTTP?

Porque o estado da partida pode mudar a qualquer momento devido às ações de outros jogadores. O WebSocket mantém uma conexão aberta e permite que o servidor envie atualizações imediatamente.

### Por que o backend precisa validar o turno se o botão já fica desativado?

Porque o front-end pode ser alterado pelo usuário. Desabilitar o botão melhora a experiência, mas somente a validação do backend protege a regra do jogo.

### Por que guardar o WebSocket em `useRef`?

Porque a conexão deve persistir entre renderizações, mas mudar essa referência não deve causar uma nova renderização.

### O que provoca a abertura do modal?

`pendingQuestion` deixar de ser `null`. O JSX usa `pendingQuestion && (...)` para renderizar o modal.

### Quem calcula a chance e o resultado do ataque?

O backend. O front apenas exibe `last_action_result` depois que recebe a resposta.

### Por que existe `matchState?.players ?? []`?

Enquanto o estado ainda não chegou, `matchState` é `null`. O optional chaining evita erro e o `?? []` fornece um array vazio que pode ser usado com `.map` e `.find`.

### Por que alguns campos aparecem no nível superior e também em `payload`?

O código parece manter compatibilidade com dois formatos de mensagem usados no protótipo. O ideal futuro seria definir um único contrato de eventos.

---

## Pontos de melhoria que você pode citar sem desvalorizar o protótipo

- padronizar todos os eventos WebSocket no formato `{ type, payload }`;
- centralizar os nomes dos eventos em constantes;
- separar o tratamento de cada evento em funções menores;
- mover a conexão WebSocket para um hook, como `useMatchWebSocket`;
- substituir `alert` por componentes visuais próprios;
- tratar erros de `JSON.parse` caso chegue uma mensagem inválida;
- usar uma URL configurável em vez de deixar `localhost:8000` fixo.

A forma correta de apresentar isso é: o componente cumpre bem a função de protótipo e demonstra o fluxo completo; essas separações seriam a evolução arquitetural para uma versão de produção.
