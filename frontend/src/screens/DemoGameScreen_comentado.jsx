/**
 * DemoGameScreen.jsx
 * -----------------------------------------------------------------------------
 * OBJETIVO DESTE COMPONENTE
 * -----------------------------------------------------------------------------
 * Esta é a tela usada para demonstrar uma partida do Polis.
 *
 * Ela possui quatro responsabilidades principais:
 *
 * 1. Abrir e manter uma conexão WebSocket com o backend.
 * 2. Receber o estado atual da partida e guardá-lo no estado do React.
 * 3. Exibir esse estado: jogadores, turno, mapa, missão e última ação.
 * 4. Enviar ao backend as escolhas feitas pelo jogador.
 *
 * IDEIA MAIS IMPORTANTE PARA A APRESENTAÇÃO:
 *
 * O FRONT-END NÃO DECIDE SE UM ATAQUE DEU CERTO.
 * Ele apenas:
 * - coleta a escolha do usuário;
 * - envia essa escolha ao backend;
 * - recebe o resultado calculado pelo backend;
 * - atualiza a interface.
 *
 * FLUXO RESUMIDO DE UMA AÇÃO:
 *
 * jogador clica no território
 *        ↓
 * jogador escolhe uma ação
 *        ↓
 * sendAttack envia "choose_attack_option"
 *        ↓
 * backend pode devolver "attack_question"
 *        ↓
 * modal mostra a pergunta
 *        ↓
 * answerAttackQuestion envia a resposta
 *        ↓
 * backend calcula o resultado
 *        ↓
 * front recebe um novo estado da partida
 *        ↓
 * React renderiza novamente a tela
 */

// Hooks utilizados pelo componente.
//
// useState: guarda informações que alteram a interface.
// useRef: guarda valores persistentes sem provocar nova renderização.
// useMemo: calcula valores derivados e reaproveita o resultado.
// useEffect: executa um efeito relacionado ao ciclo de vida do componente.
import { useEffect, useMemo, useRef, useState } from "react";

// Componente responsável por desenhar o mapa SVG do Brasil.
//
// DemoGameScreen fornece os dados dos territórios e recebe de volta o
// território selecionado pelo jogador.
import BrazilMapSvg from "../components/BrazilMapSvg.jsx";

/**
 * Relação entre a sigla de cada partido e a cor usada na interface.
 *
 * Este objeto é usado em dois lugares principais:
 * - para colorir os territórios no BrazilMapSvg;
 * - para desenhar a bolinha colorida ao lado de cada jogador.
 *
 * Como ele é uma constante externa ao componente, não é recriado a cada render.
 */
const PARTY_COLORS = {
  PR: "#E74C3C",
  PA: "#3498DB",
  PV: "#2ECC71",
  PD: "#F1C40F",
};

/**
 * Converte o objeto de missão recebido do backend em uma frase legível.
 *
 * Entrada esperada, por exemplo:
 * {
 *   type: "state",
 *   content: { state: ["SP", "RJ"] }
 * }
 *
 * Saída:
 * "Conquiste os territórios: SP, RJ."
 *
 * Esta função só formata dados. Ela não altera a missão e não verifica vitória.
 */
function formatMission(mission) {
  // Proteção contra null ou undefined enquanto a partida ainda não foi carregada.
  if (!mission) return "Missão não encontrada.";

  // Missão baseada na conquista de estados específicos.
  if (mission.type === "state") {
    // join(", ") transforma ["SP", "RJ"] em "SP, RJ".
    return `Conquiste os territórios: ${mission.content.state.join(", ")}.`;
  }

  // Missão baseada na quantidade de territórios dentro de uma ou mais regiões.
  if (mission.type === "region") {
    return mission.content.region
      // map transforma cada requisito da missão em um pequeno texto.
      .map(
        (item) =>
          `Conquiste ${item.quantity} território(s) em ${item.region}`
      )
      // join une os requisitos, caso exista mais de uma região.
      .join(" + ");
  }

  // Missão de eliminar outro jogador.
  if (mission.type === "destruction") {
    return `Destrua o jogador ${mission.content.destruction}. Se outro jogador destruí-lo antes, conquiste: ${mission.content.state.join(
      ", "
    )}.`;
  }

  // Fallback para impedir que a tela fique vazia caso chegue um tipo inesperado.
  return "Tipo de missão desconhecido.";
}

/**
 * Reduz um evento grande do WebSocket para mostrar apenas os dados mais úteis
 * no painel de log.
 *
 * O estado completo da partida pode conter muitos territórios e jogadores.
 * Mostrar tudo em cada atualização deixaria o log muito grande.
 */
function summarizeEvent(data) {
  // Optional chaining: data?.payload evita erro caso data seja null ou não
  // possua a propriedade payload.
  if (!data?.payload) return data;

  // Cria um novo objeto contendo apenas os campos importantes para depuração.
  return {
    type: data.type,
    current_turn_player_id: data.payload.current_turn_player_id,
    round: data.payload.round,
    status: data.payload.status,
    winner_id: data.payload.winner_id,
    last_action_result: data.payload.last_action_result,
  };
}

/**
 * Procura um jogador pelo ID e devolve um nome amigável para a interface.
 *
 * Exemplo:
 * getPlayerNameById("p1", players) → "Guilherme (p1)"
 */
function getPlayerNameById(playerId, players) {
  // find devolve o primeiro jogador que satisfaz a condição.
  const player = players.find((player) => player.player_id === playerId);

  // Caso o jogador seja encontrado, mostra username e ID.
  // Caso contrário, ao menos mostra o ID recebido.
  return player ? `${player.username} (${player.player_id})` : playerId;
}

/**
 * Componente principal da tela de demonstração.
 *
 * Sempre que um estado é atualizado com uma função set..., o React executa o
 * componente novamente e atualiza somente as partes necessárias da página.
 */
export default function DemoGameScreen() {
  // ---------------------------------------------------------------------------
  // 1. ESTADOS DA CONEXÃO E DA PARTIDA
  // ---------------------------------------------------------------------------

  // ID da partida digitado no campo de conexão.
  const [matchId, setMatchId] = useState("");

  // ID do jogador selecionado. A tela começa com p1 por padrão.
  const [playerId, setPlayerId] = useState("p1");

  // Indica visualmente se o WebSocket está conectado.
  const [connected, setConnected] = useState(false);

  // Guarda a representação atual da partida recebida do backend.
  // É a principal fonte de dados da interface.
  const [matchState, setMatchState] = useState(null);

  // Guarda o território em que o usuário clicou no mapa.
  const [selectedTerritory, setSelectedTerritory] = useState(null);

  // Guarda os eventos exibidos no painel de log.
  const [logs, setLogs] = useState([]);

  // ---------------------------------------------------------------------------
  // 2. ESTADOS DO MODAL DE PERGUNTA
  // ---------------------------------------------------------------------------

  // Guarda a pergunta educacional enviada pelo backend.
  // Quando deixa de ser null, o modal é exibido.
  const [pendingQuestion, setPendingQuestion] = useState(null);

  // Guarda informações da ação associada à pergunta, como território e chance.
  const [pendingActionInfo, setPendingActionInfo] = useState(null);

  // ---------------------------------------------------------------------------
  // 3. REFERÊNCIAS QUE NÃO PRECISAM CAUSAR NOVA RENDERIZAÇÃO
  // ---------------------------------------------------------------------------

  // Guarda o objeto WebSocket atual.
  //
  // Foi usado useRef porque a conexão precisa continuar existindo entre
  // renderizações, mas mudar a referência não precisa redesenhar a tela.
  const wsRef = useRef(null);

  // Impede que o alerta de vitória seja exibido repetidamente a cada novo evento.
  const winnerAlertShownRef = useRef(false);

  // ---------------------------------------------------------------------------
  // 4. DADOS DERIVADOS DO ESTADO DA PARTIDA
  // ---------------------------------------------------------------------------

  // Enquanto matchState for null, cada variável recebe um array vazio.
  // Isso permite usar .map e .find sem gerar erro.
  const players = matchState?.players ?? [];
  const territories = matchState?.territories ?? [];
  const attackOptions = matchState?.available_attack_options ?? [];

  /**
   * Descobre qual objeto de jogador representa o jogador do turno atual.
   *
   * useMemo evita repetir a busca se matchState e players não mudaram.
   * Neste componente a otimização não é indispensável, mas deixa explícito
   * que currentPlayer é um valor calculado a partir do estado da partida.
   */
  const currentPlayer = useMemo(() => {
    if (!matchState) return null;

    return players.find(
      (player) => player.player_id === matchState.current_turn_player_id
    );
  }, [matchState, players]);

  /**
   * Descobre qual jogador representa o usuário conectado nesta tela.
   *
   * O backend envia your_player_id para personalizar o estado para cada cliente.
   */
  const me = useMemo(() => {
    if (!matchState) return null;

    return players.find(
      (player) => player.player_id === matchState.your_player_id
    );
  }, [matchState, players]);

  /**
   * Regra usada pela interface para habilitar os botões de ação.
   *
   * Só é a vez do jogador quando:
   * - existe um estado da partida;
   * - a partida está em execução;
   * - o jogador atual é o mesmo jogador conectado nesta tela.
   *
   * Importante: esta validação melhora a interface, mas o backend ainda deve
   * validar o turno novamente, porque regras de segurança não podem depender
   * apenas do front-end.
   */
  const isMyTurn =
    matchState &&
    matchState.status === "running" &&
    matchState.current_turn_player_id === matchState.your_player_id;

  // ---------------------------------------------------------------------------
  // 5. FUNÇÕES AUXILIARES DA TELA
  // ---------------------------------------------------------------------------

  /**
   * Adiciona uma entrada no começo do painel de logs.
   */
  function addLog(message, data = null) {
    // A forma funcional de setLogs garante que usamos a versão mais recente
    // dos logs, mesmo quando vários eventos chegam rapidamente.
    setLogs((currentLogs) => [
      {
        // ID único usado pelo React como key na renderização da lista.
        id: crypto.randomUUID(),
        message,
        data,
        createdAt: new Date().toLocaleTimeString(),
      },

      // Mantém os logs anteriores depois do novo log.
      ...currentLogs,
    ]);
  }

  /**
   * Verifica se o novo estado representa o fim da partida e mostra o vencedor.
   */
  function handleWinnerAlert(newMatchState) {
    if (
      // A partida precisa estar finalizada.
      newMatchState.status === "finished" &&
      // Precisa existir um vencedor.
      newMatchState.winner_id &&
      // O alerta ainda não pode ter sido mostrado nesta conexão.
      !winnerAlertShownRef.current
    ) {
      // Marca imediatamente como exibido para evitar alertas duplicados.
      winnerAlertShownRef.current = true;

      // Converte o ID do vencedor em um texto com nome e ID.
      const winnerName = getPlayerNameById(
        newMatchState.winner_id,
        newMatchState.players ?? []
      );

      alert(`Fim de jogo! Vencedor: ${winnerName}`);
    }
  }

  // ---------------------------------------------------------------------------
  // 6. ABERTURA E CONTROLE DO WEBSOCKET
  // ---------------------------------------------------------------------------

  /**
   * Abre a conexão com a partida escolhida.
   *
   * O endereço contém dois parâmetros:
   * - matchId: qual partida será acessada;
   * - playerId: qual jogador esta aba representa.
   */
  function connect() {
    // trim remove espaços antes e depois do valor.
    // Sem os dois IDs, a URL da conexão ficaria incompleta.
    if (!matchId.trim() || !playerId.trim()) {
      alert("Preencha match_id e player_id.");
      return;
    }

    // Caso já exista uma conexão, ela é fechada antes da reconexão.
    // Isso evita manter dois WebSockets ativos na mesma tela.
    if (wsRef.current) {
      wsRef.current.close();
    }

    // Reinicia controles específicos da conexão anterior.
    winnerAlertShownRef.current = false;
    setPendingQuestion(null);
    setPendingActionInfo(null);

    // Cria o WebSocket apontando para a rota do backend FastAPI.
    const ws = new WebSocket(
      `wss://tcc-polis-42o9.onrender.com/ws/match/${matchId.trim()}/${playerId.trim()}`
    );

    // Guarda a conexão na referência para que outras funções possam usá-la.
    wsRef.current = ws;

    /**
     * onopen é executado quando o handshake do WebSocket é concluído.
     */
    ws.onopen = () => {
      setConnected(true);
      addLog(`Conectado como ${playerId} na partida ${matchId}`);
    };

    /**
     * onmessage é executado toda vez que o backend envia uma mensagem.
     *
     * Este é o principal ponto de entrada das atualizações da partida.
     */
    ws.onmessage = (event) => {
      // Mensagens WebSocket chegam como texto.
      // JSON.parse converte o texto JSON em objeto JavaScript.
      const data = JSON.parse(event.data);

      // Registra o evento completo para facilitar a demonstração e depuração.
      // O operador ?? usa o próximo valor quando o anterior é null/undefined.
      addLog(
        `Recebido evento: ${
          data.type ?? data.result?.type ?? "sem_tipo"
        }`,
        data
      );

      // -----------------------------------------------------------------------
      // CASO 1: O BACKEND PEDE QUE O JOGADOR RESPONDA UMA PERGUNTA
      // -----------------------------------------------------------------------
      if (data.type === "attack_question") {
        // Guardar a pergunta faz o modal aparecer no JSX final.
        setPendingQuestion(data.question);

        // Guarda os dados complementares exibidos junto da pergunta.
        setPendingActionInfo({
          target_territory_id: data.target_territory_id,
          territory_id: data.territory_id,
          territory_name: data.territory_name,
          option_id: data.option_id,
          title: data.title,
          success_chance: data.success_chance,
        });

        // O return encerra o tratamento desta mensagem.
        // Sem ele, o código continuaria testando os demais formatos.
        return;
      }

      // -----------------------------------------------------------------------
      // CASO 2: O BACKEND ENVIA UM EVENTO PADRONIZADO DE ESTADO DA PARTIDA
      // Formato esperado:
      // { type: "match_state", payload: { ...estadoDaPartida } }
      // -----------------------------------------------------------------------
      if (data.type === "match_state") {
        const newMatchState = data.payload;

        // Substitui a cópia local pelo estado mais recente vindo do servidor.
        setMatchState(newMatchState);

        // Se o novo estado já contém o resultado do ataque, a pergunta pendente
        // pode ser removida da tela.
        if (newMatchState?.last_action_result?.type === "attack_result") {
          setPendingQuestion(null);
          setPendingActionInfo(null);
        }

        // Verifica se esta atualização também encerrou a partida.
        handleWinnerAlert(newMatchState);

        return;
      }

      // -----------------------------------------------------------------------
      // CASO 3: RESPOSTA DE ATAQUE NO FORMATO { match, result }
      // -----------------------------------------------------------------------
      if (data.result?.type === "attack_result") {
        const newMatchState = data.match;

        setMatchState(newMatchState);
        setPendingQuestion(null);
        setPendingActionInfo(null);
        handleWinnerAlert(newMatchState);

        return;
      }

      // -----------------------------------------------------------------------
      // CASO 4: RESPOSTA GENÉRICA NO FORMATO { match, result }
      //
      // Este bloco aceita outros resultados que também tragam um novo estado.
      // A existência de vários formatos mostra que o front está preparado para
      // diferentes respostas do backend durante o protótipo.
      // -----------------------------------------------------------------------
      if (data.match && data.result) {
        const newMatchState = data.match;

        setMatchState(newMatchState);
        setPendingQuestion(null);
        setPendingActionInfo(null);
        handleWinnerAlert(newMatchState);

        return;
      }

      // -----------------------------------------------------------------------
      // CASO 5: ERRO ENVIADO PELO BACKEND
      // -----------------------------------------------------------------------
      if (data.type === "error") {
        // Tenta encontrar a mensagem em dois formatos possíveis.
        alert(data.payload?.message ?? data.message ?? "Erro desconhecido.");
      }
    };

    /**
     * onerror informa que ocorreu um problema na conexão.
     * O navegador normalmente fornece poucos detalhes neste callback.
     */
    ws.onerror = () => {
      addLog("Erro no WebSocket.");
    };

    /**
     * onclose é executado quando a conexão é encerrada pelo cliente, servidor
     * ou por uma falha de rede.
     */
    ws.onclose = () => {
      setConnected(false);
      addLog("Conexão fechada.");
    };
  }

  /**
   * Fecha manualmente a conexão e limpa os dados temporários da pergunta.
   */
  function disconnect() {
    if (wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
    }

    setConnected(false);
    setPendingQuestion(null);
    setPendingActionInfo(null);
  }

  // ---------------------------------------------------------------------------
  // 7. ENVIO DA ESCOLHA DE ATAQUE
  // ---------------------------------------------------------------------------

  /**
   * Envia ao backend a opção de ataque escolhida para o território selecionado.
   *
   * optionId identifica o tipo de ação clicada pelo usuário.
   */
  function sendAttack(optionId) {
    // readyState confirma que a conexão está realmente aberta.
    if (!wsRef.current || wsRef.current.readyState !== WebSocket.OPEN) {
      alert("WebSocket não está conectado.");
      return;
    }

    // Uma ação precisa de um alvo definido pelo clique no mapa.
    if (!selectedTerritory) {
      alert("Selecione um território no mapa.");
      return;
    }

    // WebSocket.send aceita texto; por isso o objeto é convertido com stringify.
    wsRef.current.send(
      JSON.stringify({
        // Tipo do evento que o handler do backend deverá reconhecer.
        type: "choose_attack_option",

        // Campos no nível superior.
        target_territory_id: selectedTerritory.territory_id,
        territory_id: selectedTerritory.territory_id,
        option_id: optionId,

        // Os mesmos campos também aparecem dentro de payload.
        // Esta duplicação provavelmente existe para compatibilidade com mais de
        // um formato de mensagem usado durante o desenvolvimento do protótipo.
        payload: {
          target_territory_id: selectedTerritory.territory_id,
          territory_id: selectedTerritory.territory_id,
          option_id: optionId,
        },
      })
    );

    addLog(
      `Enviado choose_attack_option: ${optionId} em ${selectedTerritory.territory_id}`
    );

    // Remove a seleção visual depois que a escolha foi enviada.
    setSelectedTerritory(null);
  }

  // ---------------------------------------------------------------------------
  // 8. ENVIO DA RESPOSTA À PERGUNTA
  // ---------------------------------------------------------------------------

  /**
   * Envia a resposta Verdadeiro/Falso da pergunta de ataque.
   *
   * answer será:
   * - true para Verdadeiro;
   * - false para Falso.
   */
  function answerAttackQuestion(answer) {
    if (!wsRef.current || wsRef.current.readyState !== WebSocket.OPEN) {
      alert("WebSocket não está conectado.");
      return;
    }

    wsRef.current.send(
      JSON.stringify({
        type: "answer_attack_question",

        // Resposta no nível superior.
        answer,

        // Resposta repetida dentro de payload pelo mesmo motivo de
        // compatibilidade do evento anterior.
        payload: {
          answer,
        },
      })
    );

    addLog(
      `Enviado answer_attack_question: ${
        answer ? "Verdadeiro" : "Falso"
      }`
    );

    // O modal é fechado assim que a resposta é enviada.
    // Depois disso, o backend devolverá o novo estado e o resultado da ação.
    setPendingQuestion(null);
    setPendingActionInfo(null);
  }

  // ---------------------------------------------------------------------------
  // 9. LIMPEZA AO SAIR DA TELA
  // ---------------------------------------------------------------------------

  /**
   * O array vazio [] faz este efeito ser configurado apenas uma vez.
   *
   * A função retornada é a limpeza executada quando o componente é desmontado,
   * por exemplo quando o usuário troca de página.
   */
  useEffect(() => {
    return () => {
      // Evita deixar uma conexão WebSocket aberta sem uma tela usando-a.
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, []);

  // ---------------------------------------------------------------------------
  // 10. INTERFACE JSX
  // ---------------------------------------------------------------------------
  // JSX descreve como a interface deve aparecer para o estado atual.
  // Expressões JavaScript dentro do JSX ficam entre chaves { }.

  return (
    // Elemento principal da página.
    <main className="demo-game-page">
      {/* ------------------------------------------------------------------- */}
      {/* BARRA SUPERIOR: título e controles de conexão                     */}
      {/* ------------------------------------------------------------------- */}
      <section className="demo-topbar">
        <div>
          <h1>Polis — Protótipo da Partida</h1>
          <p>Conexão direta na partida via WebSocket.</p>
        </div>

        <div className="demo-connect-panel">
          {/* Campo controlado pelo estado matchId. */}
          <label>
            Match ID
            <input
              value={matchId}
              // Cada alteração no input atualiza matchId.
              onChange={(event) => setMatchId(event.target.value)}
              placeholder="ex: 39"
            />
          </label>

          {/* Select controlado pelo estado playerId. */}
          <label>
            Player ID
            <select
              value={playerId}
              onChange={(event) => setPlayerId(event.target.value)}
            >
              <option value="p1">p1</option>
              <option value="p2">p2</option>
              <option value="p3">p3</option>
              <option value="p4">p4</option>
            </select>
          </label>

          {/* O texto muda de acordo com o estado da conexão. */}
          <button onClick={connect}>
            {connected ? "Reconectar" : "Conectar"}
          </button>

          {/* disabled impede o clique quando não existe conexão ativa. */}
          <button onClick={disconnect} disabled={!connected}>
            Desconectar
          </button>
        </div>
      </section>

      {/* Layout principal dividido em sidebar, mapa e painel de logs. */}
      <section className="demo-layout">
        {/* ----------------------------------------------------------------- */}
        {/* SIDEBAR ESQUERDA: informações e ações da partida                 */}
        {/* ----------------------------------------------------------------- */}
        <aside className="demo-sidebar">
          {/* CARD 1: informações do usuário conectado nesta aba. */}
          <div className="demo-card">
            <h2>Você</h2>
            <p>
              <strong>Jogador:</strong>{" "}
              {/* Renderização condicional usando operador ternário. */}
              {me ? `${me.username} (${me.player_id})` : "Não conectado"}
            </p>
            <p>
              <strong>Partido:</strong>{" "}
              {/* ?. evita erro; ?? mostra "-" quando não há valor. */}
              {me?.party_id ?? "-"}
            </p>
            <p>
              <strong>Status:</strong>{" "}
              {connected ? "Conectado" : "Desconectado"}
            </p>
          </div>

          {/* CARD 2: situação atual do turno e da partida. */}
          <div className="demo-card">
            <h2>Turno</h2>
            <p>
              <strong>Rodada:</strong> {matchState?.round ?? "-"}
            </p>
            <p>
              <strong>Jogador da vez:</strong>{" "}
              {currentPlayer
                ? `${currentPlayer.username} (${currentPlayer.player_id})`
                : "-"}
            </p>
            <p>
              <strong>É sua vez?</strong> {isMyTurn ? "Sim" : "Não"}
            </p>
            <p>
              <strong>Status da partida:</strong>{" "}
              {matchState?.status ?? "-"}
            </p>
            <p>
              <strong>Vencedor:</strong>{" "}
              {matchState?.winner_id
                ? getPlayerNameById(matchState.winner_id, players)
                : "Nenhum"}
            </p>
          </div>

          {/* CARD 3: missão personalizada do jogador conectado. */}
          <div className="demo-card">
            <h2>Sua missão</h2>

            {/* Versão amigável da missão. */}
            <p>{formatMission(matchState?.your_mission)}</p>

            {/* Versão JSON usada para visualizar a estrutura original. */}
            <pre>
              {JSON.stringify(matchState?.your_mission ?? null, null, 2)}
            </pre>
          </div>

          {/* CARD 4: território selecionado e botões de ataque. */}
          <div className="demo-card">
            <h2>Território selecionado</h2>

            {/*
             * Caso exista selectedTerritory, mostra seus dados e as ações.
             * Caso contrário, orienta o usuário a clicar no mapa.
             */}
            {selectedTerritory ? (
              // Fragment <> permite agrupar vários elementos sem criar uma div.
              <>
                <p>
                  <strong>{selectedTerritory.name}</strong> (
                  {selectedTerritory.territory_id})
                </p>
                <p>
                  <strong>Região:</strong> {selectedTerritory.region}
                </p>
                <p>
                  <strong>Dono:</strong> {selectedTerritory.owner_id}
                </p>
                <p>
                  <strong>Influência:</strong>{" "}
                  {selectedTerritory.current_influence}
                </p>

                <div className="demo-actions-box">
                  <h3>Ações disponíveis</h3>

                  {/* Mensagem exibida quando o backend não enviou opções. */}
                  {attackOptions.length === 0 && (
                    <p>Nenhuma ação disponível.</p>
                  )}

                  {/*
                   * Cria um botão para cada opção de ataque recebida.
                   * key ajuda o React a identificar cada item da lista.
                   */}
                  {attackOptions.map((option) => (
                    <button
                      key={option.option_id}
                      className="demo-action-button"
                      // Passa o ID específico da opção clicada.
                      onClick={() => sendAttack(option.option_id)}
                      // O botão só fica ativo durante o turno deste jogador.
                      disabled={!isMyTurn}
                    >
                      {option.title}
                      <span>
                        +{option.influence_generated} influência •{" "}
                        {option.success_chance}% sucesso • risco{" "}
                        {option.risk_level}
                      </span>
                      <small>{option.description}</small>
                    </button>
                  ))}
                </div>

                {/* && renderiza o aviso apenas quando não é o turno do usuário. */}
                {!isMyTurn && (
                  <small>Você só pode agir quando for sua vez.</small>
                )}
              </>
            ) : (
              <p>Clique em um território no mapa.</p>
            )}
          </div>

          {/* CARD 5: detalhamento do último resultado calculado pelo backend. */}
          <div className="demo-card">
            <h2>Última ação</h2>

            {matchState?.last_action_result ? (
              <>
                <p>
                  <strong>Ação:</strong>{" "}
                  {matchState.last_action_result.title}
                </p>
                <p>
                  <strong>Território:</strong>{" "}
                  {matchState.last_action_result.territory_name} (
                  {matchState.last_action_result.territory_id})
                </p>

                {/*
                 * O teste contra undefined é importante porque false é um
                 * valor válido. Usar apenas "if (question_was_correct)"
                 * esconderia justamente o caso em que a resposta foi errada.
                 */}
                {matchState.last_action_result.question_was_correct !==
                  undefined && (
                  <p>
                    <strong>Pergunta:</strong>{" "}
                    {matchState.last_action_result.question_was_correct
                      ? "Acertou"
                      : "Errou"}
                  </p>
                )}

                {/* Campo exibido somente quando veio na resposta. */}
                {matchState.last_action_result.base_success_chance !==
                  undefined && (
                  <p>
                    <strong>Chance base:</strong>{" "}
                    {matchState.last_action_result.base_success_chance}%
                  </p>
                )}

                {/* Mostra como a pergunta alterou a chance original. */}
                {matchState.last_action_result.adjusted_success_chance !==
                  undefined && (
                  <p>
                    <strong>Chance após pergunta:</strong>{" "}
                    {matchState.last_action_result.adjusted_success_chance}%
                  </p>
                )}

                <p>
                  <strong>Resultado:</strong>{" "}
                  {matchState.last_action_result.success ? "Sucesso" : "Falha"}
                </p>
                <p>
                  <strong>Conquistou?</strong>{" "}
                  {matchState.last_action_result.conquered ? "Sim" : "Não"}
                </p>
                <p>
                  <strong>Influência:</strong>{" "}
                  {matchState.last_action_result.previous_influence} →{" "}
                  {matchState.last_action_result.new_influence}
                </p>
                <p>
                  <strong>Dono:</strong>{" "}
                  {matchState.last_action_result.previous_owner_id} →{" "}
                  {matchState.last_action_result.new_owner_id}
                </p>
                <p>
                  <strong>Rolagem:</strong>{" "}
                  {matchState.last_action_result.roll}
                </p>
                <p>
                  <strong>Necessário:</strong>{" "}
                  {/*
                   * Usa minimum_roll_to_succeed quando o backend o envia.
                   * Caso seja null/undefined, calcula 100 - chance de sucesso.
                   */}
                  {matchState.last_action_result.minimum_roll_to_succeed ??
                    100 - matchState.last_action_result.success_chance}{" "}
                  ou mais
                </p>
                <p>
                  <strong>Chance de sucesso:</strong>{" "}
                  {matchState.last_action_result.success_chance}%
                </p>
              </>
            ) : (
              <p>Nenhuma ação realizada ainda.</p>
            )}
          </div>

          {/* CARD 6: lista de jogadores presentes na partida. */}
          <div className="demo-card">
            <h2>Jogadores</h2>

            <div className="demo-players">
              {players.map((player) => (
                <div key={player.player_id} className="demo-player">
                  <span
                    className="demo-color-dot"
                    style={{
                      // Procura a cor do partido; usa cinza como fallback.
                      backgroundColor:
                        PARTY_COLORS[player.party_id] ?? "#999",
                    }}
                  />
                  <span>
                    {player.username} — {player.player_id} — {player.party_id}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </aside>

        {/* ----------------------------------------------------------------- */}
        {/* MAPA CENTRAL                                                     */}
        {/* ----------------------------------------------------------------- */}
        <section className="demo-map-area">
          <BrazilMapSvg
            // Dados usados para representar dono, influência e outros estados.
            territories={territories}
            // Permite ao mapa relacionar owner_id aos dados dos jogadores.
            players={players}
            // Define a cor de cada partido.
            partyColors={PARTY_COLORS}
            // Informa qual território deve aparecer visualmente selecionado.
            selectedTerritoryId={selectedTerritory?.territory_id}
            // O mapa chama esta função quando o usuário clica em um território.
            // Assim, o filho BrazilMapSvg atualiza o estado do componente pai.
            onSelectTerritory={setSelectedTerritory}
            className="demo-map"
          />
        </section>

        {/* ----------------------------------------------------------------- */}
        {/* PAINEL DIREITO: LOG DE COMUNICAÇÃO                               */}
        {/* ----------------------------------------------------------------- */}
        <aside className="demo-log-panel">
          <h2>Log</h2>

          {/* Renderiza uma entrada para cada log armazenado. */}
          {logs.map((log) => (
            <div key={log.id} className="demo-log-item">
              <strong>
                [{log.createdAt}] {log.message}
              </strong>

              {/*
               * Eventos com payload costumam carregar o estado inteiro.
               * summarizeEvent reduz o conteúdo antes de mostrá-lo.
               */}
              {log.data?.payload && (
                <pre>{JSON.stringify(summarizeEvent(log.data), null, 2)}</pre>
              )}

              {/*
               * Para outros formatos de evento, exibe o objeto completo.
               * O segundo argumento null não usa função de substituição.
               * O terceiro argumento 2 cria indentação de dois espaços.
               */}
              {!log.data?.payload && log.data && (
                <pre>{JSON.stringify(log.data, null, 2)}</pre>
              )}
            </div>
          ))}
        </aside>
      </section>

      {/* ------------------------------------------------------------------- */}
      {/* MODAL DA PERGUNTA                                                  */}
      {/* ------------------------------------------------------------------- */}
      {/*
       * O modal só existe no DOM quando pendingQuestion não é null.
       * Portanto, atualizar pendingQuestion controla sua abertura e fechamento.
       */}
      {pendingQuestion && (
        <div className="question-modal-backdrop">
          <div className="question-modal">
            <h2>Pergunta</h2>

            <p className="question-subject">{pendingQuestion.subject}</p>

            <p className="question-description">
              {pendingQuestion.description}
            </p>

            {/* Informações da ação aparecem apenas quando também estão salvas. */}
            {pendingActionInfo && (
              <div className="question-action-info">
                <p>
                  <strong>Ação:</strong> {pendingActionInfo.title}
                </p>

                <p>
                  <strong>Território:</strong>{" "}
                  {pendingActionInfo.territory_name}
                </p>

                <p>
                  <strong>Chance base:</strong>{" "}
                  {pendingActionInfo.success_chance}%
                </p>
              </div>
            )}

            <div className="question-buttons">
              {/* true representa a resposta Verdadeiro. */}
              <button onClick={() => answerAttackQuestion(true)}>
                Verdadeiro
              </button>

              {/* false representa a resposta Falso. */}
              <button onClick={() => answerAttackQuestion(false)}>
                Falso
              </button>
            </div>
          </div>
        </div>
      )}
    </main>
  );
}
