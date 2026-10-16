import { useEffect, useMemo, useRef, useState } from "react";

import BrazilMapSvg from "../components/BrazilMapSvg.jsx";
import { getAvatarImage } from "../utils/avatarAssets.js";
import QUESTION_PREVIEW_BANK from "../data/questionPreviewBank.json";

const PARTY_COLORS = {
  PR: "#DA3A3C",
  PA: "#28A3E0",
  PV: "#30C067",
  PD: "#E0A12A",
};

const QUESTION_SUBJECT_LABELS = {
  philosophy: "Filosofia",
  sociology: "Sociologia",
  geography: "Geografia",
  history: "História",
};

const QUESTION_DIFFICULTY_LABELS = {
  easy: "Fácil",
  medium: "Médio",
  hard: "Difícil",
};

function QuestionPresentation({
  question,
  targetName,
  onAnswer,
  onDismiss,
  isDemo = false,
}) {
  const [selectedAnswer, setSelectedAnswer] = useState(null);
  const [remainingSeconds, setRemainingSeconds] = useState(30);

  useEffect(() => {
    if (remainingSeconds <= 0 || (isDemo && selectedAnswer !== null)) return undefined;

    const timeoutId = window.setTimeout(() => {
      setRemainingSeconds((current) => Math.max(0, current - 1));
    }, 1000);

    return () => window.clearTimeout(timeoutId);
  }, [isDemo, remainingSeconds, selectedAnswer]);

  if (!question) return null;

  const timerMinutes = String(Math.floor(remainingSeconds / 60)).padStart(2, "0");
  const timerSeconds = String(remainingSeconds % 60).padStart(2, "0");

  function handleAnswer(letter) {
    if (isDemo) {
      setSelectedAnswer(letter);
      return;
    }
    onAnswer(letter);
  }

  return (
    <div
      className="polis-question-preview-overlay"
      role="dialog"
      aria-modal="true"
      aria-label={isDemo ? "Tela demonstrativa de pergunta" : "Pergunta da partida"}
      onClick={isDemo ? onDismiss : undefined}
    >
      <section
        className="polis-question-preview-box"
        onClick={isDemo ? (event) => event.stopPropagation() : undefined}
      >
        <img className="polis-question-preview-bg" src="/areapergunta.png" alt="" />
        <div className="polis-question-preview-top-row">
          {targetName && (
            <span className="polis-question-preview-target">Alvo: {targetName}</span>
          )}
          <div
            className="polis-question-preview-timer"
            role="timer"
            aria-label={`Tempo restante: ${timerMinutes}:${timerSeconds}`}
          >
            {timerMinutes}:{timerSeconds}
          </div>
        </div>
        <div className="polis-question-preview-tags">
          <span>{QUESTION_SUBJECT_LABELS[String(question.subject ?? "").toLowerCase()] ?? question.subject}</span>
          {question.difficulty && (
            <span>{QUESTION_DIFFICULTY_LABELS[String(question.difficulty).toLowerCase()] ?? question.difficulty}</span>
          )}
          <span className="polis-question-preview-chance-tag">
            Chance de sucesso: +20%
          </span>
        </div>
        <div className="polis-question-preview-content">
          <div className="polis-question-preview-main">
            <div className="polis-question-preview-body">
              <p className="polis-question-preview-title">
                {question.question_id ?? 1}) {question.exam_board ? `(${question.exam_board})` : ""}
              </p>
              <p>{question.description}</p>
            </div>
            <div className="polis-question-preview-answers">
              {Object.entries(question.options ?? {}).map(([letter, text]) => (
                <button
                  type="button"
                  key={letter}
                  onClick={() => handleAnswer(letter)}
                  disabled={isDemo && selectedAnswer !== null}
                  className={
                    isDemo && selectedAnswer !== null
                      ? selectedAnswer === question.answer && letter === question.answer
                        ? "is-correct"
                        : letter === selectedAnswer
                          ? "is-incorrect"
                          : ""
                      : ""
                  }
                >
                  {letter}) {text}
                </button>
              ))}
            </div>
          </div>
          {question.explanation && (!isDemo || selectedAnswer !== null) && (
            <div className="polis-question-preview-explanation">
              <p>Explicação:</p>
              <span>{question.explanation}</span>
            </div>
          )}
        </div>
      </section>
    </div>
  );
}

function getPlayerNameById(playerId, players) {
  const player = players.find((item) => item.player_id === playerId);
  return player?.username ?? playerId ?? "jogador desconhecido";
}


function formatMission(mission, players = []) {
  if (!mission) {
    return "Missão não encontrada.";
  }

  const content = mission.content ?? {};

  if (mission.type === "state") {
    const states = content.state ?? [];

    if (states.length === 0) {
      return "Conquiste os territórios indicados pela sua missão.";
    }

    return `Conquiste os territórios: ${states.join(", ")}.`;
  }

  if (mission.type === "region") {
    const regions = content.region ?? [];

    if (regions.length === 0) {
      return "Conquiste os territórios indicados pela sua missão.";
    }

    return regions
      .map(
        (item) =>
          `Conquiste ${item.quantity} território(s) em ${item.region}`
      )
      .join(" + ");
  }

  if (mission.type === "destruction") {
    const targetPlayerId = content.destruction;
    const alternativeStates = content.state ?? [];

    if (targetPlayerId) {
      const targetName = getPlayerNameById(targetPlayerId, players);

      if (alternativeStates.length > 0) {
        return `Destrua o jogador ${targetName}. Se essa missão for convertida, conquiste: ${alternativeStates.join(
          ", "
        )}.`;
      }

      return `Destrua o jogador ${targetName}.`;
    }

    if (alternativeStates.length > 0) {
      return `Conquiste os territórios: ${alternativeStates.join(", ")}.`;
    }

    return "Elimine o jogador indicado pela sua missão.";
  }

  return "Tipo de missão desconhecido.";
}

function PlayerCard({
  player,
  isCurrentTurn,
  isNext,
  isMe,
  partyColors,
  territories = [],
  side = "left",
}) {
  if (!player) {
    return null;
  }

  const partyColor = partyColors[player.party_id] ?? "#7f8c8d";

  const initials =
    player.username
      ?.trim()
      .split(/\s+/)
      .map((name) => name[0])
      .join("")
      .slice(0, 2)
      .toUpperCase() || "?";

  const controlledTerritories = territories.filter((territory) => territory.owner_id === player.player_id).length;
  const imageSuffix = side === "right" ? "d" : "e";

  return (
    <div
      className={[
        "polis-player-card",
        `polis-player-card-${side}`,
        isCurrentTurn ? "polis-player-current" : "",
        isMe ? "polis-player-me" : "",
      ]
        .filter(Boolean)
        .join(" ")}
      style={{ "--party-color": partyColor }}
    >
      <img
        className="polis-player-curtain"
        src="/Cortina.png"
        alt=""
        aria-hidden="true"
      />
      <div className="polis-player-polygon" aria-hidden="true" />
{isNext && <div className="polis-next-label">Próximo</div>}


      <div className="polis-player-main">
        <div className="polis-player-avatar">
          <img
            src={getAvatarImage(player.avatar_id)}
            alt={`Avatar de ${player.username}`}
            onError={(event) => {
              event.currentTarget.src = getAvatarImage("avatar_3");
            }}
          />
        </div>

        <div className="polis-player-stats">
          <div className="polis-stat-row polis-stat-corruption" style={{ backgroundImage: `url(/corrupcao${imageSuffix}.png)` }}><span>{player.match_corruption ?? 0}%</span></div>
          <div className="polis-stat-row polis-stat-money" style={{ backgroundImage: `url(/dinheiro${imageSuffix}.png)` }}><span>{player.match_money ?? 0}$</span></div>
          <div className="polis-stat-row polis-stat-states" style={{ backgroundImage: `url(/estados${imageSuffix}.png)` }}><span>{controlledTerritories}</span></div>
        </div>
      </div>
      <div className="polis-player-name">{player.username}</div>
    </div>
  );
}

function LastActionResult({ result }) {
  if (!result) {
    return (
      <section className="polis-last-action-section">
        <div className="polis-last-action-card">
          <h2>Última ação</h2>

          <p className="polis-last-action-empty">
            Nenhuma ação realizada ainda.
          </p>
        </div>
      </section>
    );
  }

  const formatValue = (value) => {
    const number = Number(value ?? 0);

    if (number > 0) {
      return `+${number}`;
    }

    return String(number);
  };

  return (
    <section className="polis-last-action-section">

      <div
        className={[
          "polis-last-action-card",
          result.success
            ? "polis-action-success"
            : "polis-action-failure",
        ].join(" ")}
      >

        <div className="polis-last-action-header">

          <div>
            <span className="polis-last-action-label">
              Última ação
            </span>

            <h2>
              {result.title ?? "Ação realizada"}
            </h2>
          </div>

          <span className="polis-last-action-status">
            {result.success
              ? "SUCESSO"
              : "FALHA"}
          </span>

        </div>


        <div className="polis-last-action-content">

          {result.type && (
            <p>
              <span>Tipo:</span>{" "}
              {result.type}
            </p>
          )}


          {result.territory_name && (
            <p>
              <span>Território:</span>{" "}
              {result.territory_name}
            </p>
          )}


          {result.response && (
            <p className="polis-last-action-response">
              {result.response}
            </p>
          )}


          <div className="polis-last-action-values">

            {Number(result.influence_generated ?? 0) !== 0 && (
              <div>
                <span>Influência</span>

                <span>
                  {formatValue(
                    result.influence_generated
                  )}
                </span>
              </div>
            )}


            {Number(result.money_generated ?? 0) !== 0 && (
              <div>
                <span>Dinheiro</span>

                <span>
                  {formatValue(
                    result.money_generated
                  )}
                </span>
              </div>
            )}


            {Number(result.corruption_generated ?? 0) !== 0 && (
              <div>
                <span>Corrupção</span>

                <span>
                  {formatValue(
                    result.corruption_generated
                  )}
                </span>
              </div>
            )}

          </div>


          <div className="polis-last-action-details">

            {result.conquered === true && (
              <p>
                ✓ Território conquistado
              </p>
            )}


            {result.question_was_correct === true && (
              <p>
                ✓ Pergunta respondida corretamente
              </p>
            )}


            {result.question_was_correct === false && (
              <p>
                ✕ Pergunta respondida incorretamente
              </p>
            )}

          </div>

        </div>

      </div>

    </section>
  );
}


export default function DemoGameScreen({
  onReturnRoom,
  initialMatchId,
  initialPlayerId,
  onMatchNotFound,
  onLeaveRoom,
}) {
  const matchId = String(initialMatchId ?? "");
  const playerId = initialPlayerId ?? "";

  const [connected, setConnected] = useState(false);
  const [matchState, setMatchState] = useState(null);

  const [lastActionResult, setLastActionResult] = useState(null);

  const [selectedTerritory, setSelectedTerritory] = useState(null);
  const [showInitialDistribution, setShowInitialDistribution] = useState(false);
  const [distributionConfirmed, setDistributionConfirmed] = useState(false);
  const [distributionTerritoryId, setDistributionTerritoryId] = useState("");
  const [distributionAmount, setDistributionAmount] = useState(200);
  const [showVictoryScreen, setShowVictoryScreen] = useState(false);
  const [showQuestionPreview, setShowQuestionPreview] = useState(false);
  const [previewQuestion, setPreviewQuestion] = useState(null);
  const [availableActions, setAvailableActions] = useState([]);
  const [actionType, setActionType] = useState(null);

  const [pendingQuestion, setPendingQuestion] = useState(null);
  const [pendingActionInfo, setPendingActionInfo] = useState(null);
  const [gameNotice, setGameNotice] = useState(null);
  const [skipTurnMessage, setSkipTurnMessage] = useState(null);


  const wsRef = useRef(null);
  const winnerAlertShownRef = useRef(false);
  const reconnectTimerRef = useRef(null);
  const gameNoticeTimerRef = useRef(null);
  const skipTurnTimerRef = useRef(null);
  const lastSkippedTurnRef = useRef(null);
  const lastActionNoticeRef = useRef(null);
  const gameNoticeIdRef = useRef(0);
  const localActionPendingRef = useRef(false);
  const receivedInitialStateRef = useRef(false);
  const shouldReconnectRef = useRef(true);
  const isUnmountingRef = useRef(false);

  const players = matchState?.players ?? [];
  const territories = matchState?.territories ?? [];
  const myTerritories = territories.filter(
    (territory) => territory.owner_id === matchState?.your_player_id
  );
  const distributionTerritory =
    myTerritories.find((territory) => territory.territory_id === distributionTerritoryId) ??
    myTerritories[0] ??
    null;

  function showGameNotice(kind, message) {
    showGameNotices([{ kind, message }]);
  }

  function showGameNotices(notices) {
    if (!notices.length) return;

    if (gameNoticeTimerRef.current) {
      clearTimeout(gameNoticeTimerRef.current);
    }

    let noticeIndex = 0;
    const showNextNotice = () => {
      setGameNotice({ ...notices[noticeIndex], id: ++gameNoticeIdRef.current });
      gameNoticeTimerRef.current = setTimeout(() => {
        noticeIndex += 1;
        if (noticeIndex < notices.length) {
          showNextNotice();
        } else {
          setGameNotice(null);
          gameNoticeTimerRef.current = null;
        }
      }, 2200);
    };

    showNextNotice();
  }

  function notifyActionCompleted(result) {
    if (!["attack_result", "attack_no_question"].includes(result?.type)) {
      return;
    }

    const signature = JSON.stringify(result);
    if (receivedInitialStateRef.current && signature !== lastActionNoticeRef.current && localActionPendingRef.current) {
      const notices = [];
      if (typeof result.question_was_correct === "boolean") {
        notices.push({
          kind: result.question_was_correct ? "success" : "error",
          message: result.question_was_correct ? "Resposta correta!" : "Resposta errada!",
        });
      }
      notices.push({ kind: "success", message: "Ação concluída!" });
      showGameNotices(notices);
      localActionPendingRef.current = false;
    }
    lastActionNoticeRef.current = signature;
  }

  const currentPlayer = useMemo(() => {
    if (!matchState) {
      return null;
    }

    return (
      players.find(
        (player) =>
          player.player_id === matchState.current_turn_player_id
      ) ?? null
    );
  }, [matchState, players]);

  const me = useMemo(() => {
    if (!matchState) {
      return null;
    }

    return (
      players.find(
        (player) => player.player_id === matchState.your_player_id
      ) ?? null
    );
  }, [matchState, players]);

  const maxDistributionInfluence = Math.max(
    0,
    Number(me?.match_influence ?? 0)
  );
  const distributionAmountValue =
    distributionAmount === ""
      ? 0
      : Math.min(
          maxDistributionInfluence,
          Math.max(0, Number(distributionAmount) || 0)
        );

  const isMyTurn =
    Boolean(matchState) &&
    matchState.status === "running" &&
    matchState.current_turn_player_id === matchState.your_player_id;

  const nextPlayer = useMemo(() => {
    if (players.length === 0 || !matchState?.current_turn_player_id) {
      return null;
    }

    const currentIndex = players.findIndex(
      (player) =>
        player.player_id === matchState.current_turn_player_id
    );

    if (currentIndex === -1) {
      return null;
    }

    return players[(currentIndex + 1) % players.length] ?? null;
  }, [players, matchState?.current_turn_player_id]);

  const playerPositions = useMemo(() => {
    // IMPORTANTE:
    // os cards ficam sempre nas mesmas posições.
    // A troca de turno altera apenas o destaque e o rótulo "Próximo".
    return players.slice(0, 4);
  }, [players]);

  const victoryRanking = useMemo(() => {
    const rankedPlayers = players.map((player) => ({
      ...player,
      controlledTerritories: territories.filter(
        (territory) => territory.owner_id === player.player_id
      ).length,
    }));
    const winnerId = matchState?.winner_id;

    return rankedPlayers.sort((a, b) => {
      if (winnerId && a.player_id === winnerId) return -1;
      if (winnerId && b.player_id === winnerId) return 1;
      return (
        b.controlledTerritories - a.controlledTerritories ||
        (b.match_money ?? 0) - (a.match_money ?? 0) ||
        (b.match_influence ?? 0) - (a.match_influence ?? 0)
      );
    });
  }, [players, territories, matchState?.winner_id]);

  const victoryWinner = victoryRanking[0] ?? null;

  function handleWinnerAlert(newMatchState) {
    if (
      newMatchState?.status === "finished" &&
      newMatchState?.winner_id &&
      !winnerAlertShownRef.current
    ) {
      winnerAlertShownRef.current = true;

      const winnerName = getPlayerNameById(
        newMatchState.winner_id,
        newMatchState.players ?? []
      );

      setShowVictoryScreen(true);
    }
  }

  function connect() {
    if (!matchId || !playerId) {
      console.error("matchId ou playerId não disponíveis.");
      return;
    }

    // Não cria outra conexão se já existir uma ativa.
    if (
      wsRef.current &&
      (
        wsRef.current.readyState === WebSocket.OPEN ||
        wsRef.current.readyState === WebSocket.CONNECTING
      )
    ) {
      return;
    }

    const WS =
      import.meta.env.VITE_WS_URL ||
      "wss://tcc-polis-42o9.onrender.com";

    console.log(
      `Conectando na partida ${matchId} como ${playerId}...`
    );

    const ws = new WebSocket(
      `${WS}/ws/match/${matchId}/${playerId}`
    );

    wsRef.current = ws;

    ws.onopen = () => {
      console.log("WebSocket conectado.");

      setConnected(true);

      // Se havia uma tentativa de reconexão pendente,
      // ela não é mais necessária.
      if (reconnectTimerRef.current) {
        clearTimeout(reconnectTimerRef.current);
        reconnectTimerRef.current = null;
      }
    };

    ws.onmessage = (event) => {
      let data;

      try {
        data = JSON.parse(event.data);
      } catch (error) {
        console.error(
          "Erro ao interpretar mensagem WebSocket:",
          error
        );

        return;
      }

      console.log("Evento recebido:", data);

      if (data.type === "territory_selected") {
        console.log("Território selecionado:", data.payload);

        setSelectedTerritory(
          data.payload.territory
        );

        setAvailableActions(
          data.payload.available_actions
        );

        setActionType(
          data.payload.action_type
        );

        return;
      }

      if (data.type === "attack_question") {
        setPendingQuestion(data.question);

        setPendingActionInfo({
          target_territory_id:
            data.target_territory_id,

          territory_id:
            data.territory_id,

          territory_name:
            data.territory_name,

          option_id:
            data.option_id,

          title:
            data.title,

          success_chance:
            data.success_chance,
        });

        return;
      }

      if (data.type === "match_state") {
        const newMatchState = data.payload;
        const actionResult = newMatchState?.last_action_result;
        const skippedPlayerId = newMatchState?.skipped_player_id ?? null;

        if (!skippedPlayerId || !receivedInitialStateRef.current) {
          lastSkippedTurnRef.current = null;
        } else {
          const skippedTurnKey = `${skippedPlayerId}:${newMatchState?.current_turn_player_id ?? ""}`;
          if (lastSkippedTurnRef.current !== skippedTurnKey) {
            lastSkippedTurnRef.current = skippedTurnKey;
            const skippedPlayer = newMatchState.players?.find(
              (player) => player.player_id === skippedPlayerId
            );
            setSkipTurnMessage(
              `${skippedPlayer?.username ?? "O jogador"} não possui dinheiro suficiente. A vez foi pulada.`
            );
            if (skipTurnTimerRef.current) {
              clearTimeout(skipTurnTimerRef.current);
            }
            skipTurnTimerRef.current = setTimeout(() => {
              setSkipTurnMessage(null);
              skipTurnTimerRef.current = null;
            }, 5000);
          }
        }

        if (receivedInitialStateRef.current) {
          notifyActionCompleted(actionResult);
        } else if (["attack_result", "attack_no_question"].includes(actionResult?.type)) {
          lastActionNoticeRef.current = JSON.stringify(actionResult);
        }
        receivedInitialStateRef.current = true;

        setMatchState(newMatchState);

        // Atualiza o painel de última ação
        if (newMatchState?.last_action_result) {
          setLastActionResult(
            newMatchState.last_action_result
          );
        }

        if (
          newMatchState?.last_action_result?.type ===
          "attack_result"
        ) {
          setPendingQuestion(null);
          setPendingActionInfo(null);
        }

        handleWinnerAlert(newMatchState);

        return;
      }


      if (data.result?.type === "attack_result") {
        const newMatchState = data.match;

        notifyActionCompleted(data.result);

        setMatchState(newMatchState);

        // Atualiza o painel imediatamente
        setLastActionResult(data.result);

        setPendingQuestion(null);
        setPendingActionInfo(null);

        handleWinnerAlert(newMatchState);

        return;
      }


      if (data.match && data.result) {
        const newMatchState = data.match;

        notifyActionCompleted(data.result);

        setMatchState(newMatchState);

        // Atualiza o painel imediatamente
        setLastActionResult(data.result);

        setPendingQuestion(null);
        setPendingActionInfo(null);

        handleWinnerAlert(newMatchState);

        return;
      }

      if (data.type === "error") {
        const message =
          data.payload?.message ??
          data.message ??
          "Erro desconhecido.";

        console.error("Erro recebido do servidor:", message);

        /*
         * IMPORTANTE:
         *
         * Um erro de jogada NÃO deve derrubar a conexão.
         * Apenas mostramos o erro.
         */
        const normalizedMessage = message.toLowerCase();
        if (
          (normalizedMessage.includes("partida") && normalizedMessage.includes("encontrada")) ||
          normalizedMessage.includes("match not found")
        ) {
          onMatchNotFound?.(message);
          return;
        }

        if (normalizedMessage.includes("fronteira")) {
          localActionPendingRef.current = false;
          setSelectedTerritory(null);
          setAvailableActions([]);
          return;
        }

        const isTechnicalError =
          normalizedMessage.includes("not supported between instances") ||
          normalizedMessage.includes("nonetype") ||
          normalizedMessage.includes("traceback");
        showGameNotice(
          "error",
          isTechnicalError ? "Não foi possível concluir a ação. Tente novamente." : message
        );
        localActionPendingRef.current = false;

        return;
      }
    };

    ws.onerror = (error) => {
      console.error("Erro no WebSocket:", error);

      /*
       * Não chamamos ws.close() aqui.
       *
       * Deixamos o navegador disparar onclose
       * caso a conexão realmente tenha caído.
       */
    };

    ws.onclose = (event) => {
      console.log(
        "WebSocket fechado:",
        event.code,
        event.reason
      );

      setConnected(false);

      if (wsRef.current === ws) {
        wsRef.current = null;
      }

      /*
       * Se a tela ainda está aberta e não foi uma
       * desconexão intencional, tenta reconectar.
       */
      if (
        shouldReconnectRef.current &&
        !isUnmountingRef.current
      ) {
        console.log(
          "Tentando reconectar em 2 segundos..."
        );

        reconnectTimerRef.current =
          setTimeout(() => {
            connect();
          }, 2000);
      }
    };
  }

  function handleTerritorySelection(territory) {
    setSelectedTerritory(territory);

    if (
      !wsRef.current ||
      wsRef.current.readyState !== WebSocket.OPEN
    ) {
      return;
    }

    wsRef.current.send(
      JSON.stringify({
        type: "select_territory",
        territory_id: territory.territory_id,

        payload: {
          territory_id: territory.territory_id,
        },
      })
    );
  }

  function sendAttack(optionId, action_type) {
    console.log("ACTION ID:", optionId);
    if (
      !wsRef.current ||
      wsRef.current.readyState !== WebSocket.OPEN
    ) {
      alert("WebSocket não está conectado.");
      return;
    }

    if (!selectedTerritory) {
      alert("Selecione um território no mapa.");
      return;
    }

    localActionPendingRef.current = true;
    wsRef.current.send(
      JSON.stringify({
        type: "choose_attack_option",

        target_territory_id: selectedTerritory.territory_id,
        territory_id: selectedTerritory.territory_id,
        action_id: optionId,
        action_type: action_type,

        payload: {
          target_territory_id: selectedTerritory.territory_id,
          territory_id: selectedTerritory.territory_id,
          action_id: optionId,
          action_type: action_type,
        },
      })
    );

    setSelectedTerritory(null);
  }

  function answerAttackQuestion(answer) {
    if (
      !wsRef.current ||
      wsRef.current.readyState !== WebSocket.OPEN
    ) {
      alert("WebSocket não está conectado.");
      return;
    }

    wsRef.current.send(
      JSON.stringify({
        type: "answer_attack_question",
        answer,

        payload: {
          answer,
        },
      })
    );

    setPendingQuestion(null);
    setPendingActionInfo(null);
  }

  useEffect(() => {
    if (!matchId || !playerId) {
      return;
    }

    isUnmountingRef.current = false;
    shouldReconnectRef.current = true;

    connect();

    return () => {
      isUnmountingRef.current = true;
      shouldReconnectRef.current = false;

      if (reconnectTimerRef.current) {
        clearTimeout(reconnectTimerRef.current);

        reconnectTimerRef.current = null;
      }

      if (gameNoticeTimerRef.current) {
        clearTimeout(gameNoticeTimerRef.current);
        gameNoticeTimerRef.current = null;
      }

      if (skipTurnTimerRef.current) {
        clearTimeout(skipTurnTimerRef.current);
        skipTurnTimerRef.current = null;
      }

      if (wsRef.current) {
        wsRef.current.close();

        wsRef.current = null;
      }
    };
  }, [matchId, playerId]);

  const missionText = formatMission(
    matchState?.your_mission,
    players
  );

  return (
    <div className={`polis-game-page${showVictoryScreen ? " polis-victory-opened" : ""}`}>
      {skipTurnMessage && (
        <div className="polis-skip-turn-message" role="status" aria-live="polite">
          {skipTurnMessage}
        </div>
      )}
      {!showVictoryScreen && (
        <button
          type="button"
          className="polis-victory-open"
          onClick={() => setShowVictoryScreen(true)}
          aria-label="Abrir tela de vitória"
        >
          <img src="/coroa.png" alt="" />
          Vitória
        </button>
      )}
      {!showInitialDistribution && !showVictoryScreen && (
        <button
          type="button"
          className="polis-victory-open polis-distribution-open"
          onClick={() => {
            setDistributionConfirmed(false);
            setShowInitialDistribution(true);
          }}
          aria-label="Abrir distribuição"
        >
          <span className="polis-distribution-open-icon" aria-hidden="true">+</span>
          Distribuição
        </button>
      )}
      {!showVictoryScreen && !showQuestionPreview && (
        <button
          type="button"
          className="polis-victory-open polis-question-preview-open"
          onClick={() => {
            const randomIndex = Math.floor(Math.random() * QUESTION_PREVIEW_BANK.length);
            setPreviewQuestion(QUESTION_PREVIEW_BANK[randomIndex]);
            setShowQuestionPreview(true);
          }}
          aria-label="Abrir tela demonstrativa de pergunta"
        >
          <span className="polis-question-preview-icon" aria-hidden="true">?</span>
          Pergunta
        </button>
      )}

      <main className="polis-game-screen">
        <div className="polis-turn-title">
          Vez de{" "}
          <span
            style={{
              color:
                PARTY_COLORS[currentPlayer?.party_id] ?? "#ffffff",
            }}
          >
            {currentPlayer?.username ?? "..."}
          </span>
        </div>

        <div className="polis-position polis-position-top-left">
          <PlayerCard
            player={playerPositions[0]}
            isCurrentTurn={
              playerPositions[0]?.player_id ===
              matchState?.current_turn_player_id
            }
            isNext={
              playerPositions[0]?.player_id ===
              nextPlayer?.player_id
            }
            isMe={
              playerPositions[0]?.player_id ===
              matchState?.your_player_id
            }
            partyColors={PARTY_COLORS}
            territories={territories}
            side="left"
          />
        </div>

        <div className="polis-position polis-position-top-right">
          <PlayerCard
            player={playerPositions[1]}
            isCurrentTurn={
              playerPositions[1]?.player_id ===
              matchState?.current_turn_player_id
            }
            isNext={
              playerPositions[1]?.player_id ===
              nextPlayer?.player_id
            }
            isMe={
              playerPositions[1]?.player_id ===
              matchState?.your_player_id
            }
            partyColors={PARTY_COLORS}
            territories={territories}
            side="right"
          />
        </div>

        <div className="polis-position polis-position-bottom-left">
          <PlayerCard
            player={playerPositions[2]}
            isCurrentTurn={
              playerPositions[2]?.player_id ===
              matchState?.current_turn_player_id
            }
            isNext={
              playerPositions[2]?.player_id ===
              nextPlayer?.player_id
            }
            isMe={
              playerPositions[2]?.player_id ===
              matchState?.your_player_id
            }
            partyColors={PARTY_COLORS}
            territories={territories}
            side="left"
          />
        </div>

        <div className="polis-position polis-position-bottom-right">
          <PlayerCard
            player={playerPositions[3]}
            isCurrentTurn={
              playerPositions[3]?.player_id ===
              matchState?.current_turn_player_id
            }
            isNext={
              playerPositions[3]?.player_id ===
              nextPlayer?.player_id
            }
            isMe={
              playerPositions[3]?.player_id ===
              matchState?.your_player_id
            }
            partyColors={PARTY_COLORS}
            territories={territories}
            side="right"
          />
        </div>

        <section className="polis-map-container">
          <img
            className="polis-america-backdrop"
            src="/AMERICA.png"
            alt=""
            aria-hidden="true"
          />
          <BrazilMapSvg
            territories={territories}
            players={players}
            partyColors={PARTY_COLORS}
            currentPlayerId={matchState?.your_player_id}
            selectedTerritoryId={
              selectedTerritory?.territory_id
            }
            isActionable={isMyTurn}
            onSelectTerritory={handleTerritorySelection}
            className="polis-main-map"
          />
        </section>

        <aside className="polis-mission-card polis-mission-right">
          <img className="polis-mission-art" src="/missaosec.png" alt="Missão Secreta" />
          <div className="polis-mission-copy">
            <p>{missionText}</p>
          </div>
        </aside>

        {selectedTerritory && (
          <div className="polis-choice-overlay">
            <section className="polis-choice-board" aria-label="Escolhas do território">
              <header className="polis-choice-board-header">
                <div className="polis-choice-territory">
                  <h2>
                    {selectedTerritory.name &&
                    selectedTerritory.name !== selectedTerritory.territory_id
                      ? `${selectedTerritory.name} (${selectedTerritory.territory_id})`
                      : selectedTerritory.territory_id}
                  </h2>
                  <span>{selectedTerritory.region ?? "-"}</span>
                </div>
                <div className="polis-choice-influence">
                  <span>Influência</span>
                  <span>{selectedTerritory.current_influence ?? 0}</span>
                </div>
              </header>

              {isMyTurn ? (
                <div className="polis-choice-cards">
                  {availableActions.length === 0 && (
                    <p className="polis-no-choice">Nenhuma ação disponível.</p>
                  )}
                  {availableActions.slice(0, 4).map((option) => (
                    <button
                      type="button"
                      className="polis-choice-card"
                      key={option.action_id}
                      onClick={() => sendAttack(option.action_id, option.action_type)}
                    >
                      <span className="polis-choice-card-title">
                        <strong>{option.title}</strong>
                      </span>
                      <span className="polis-choice-card-risk">
                        {({
                          low: "Risco baixo",
                          medium: "Risco médio",
                          high: "Risco alto",
                          insane: "Risco insano",
                        })[option.risk_level] ?? option.risk_level ?? "Risco não informado"}
                      </span>
                      <span className="polis-choice-card-details">
                        {option.influence_generated !== undefined && (
                          <span>+{option.influence_generated} influência</span>
                        )}
                        {option.success_chance !== undefined && (
                          <span className="polis-choice-success">{option.success_chance}% de sucesso</span>
                        )}
                        {option.description && (
                          <span className="polis-choice-description">{option.description}</span>
                        )}
                      </span>
                      {option.cost !== undefined && (
                        <span className="polis-choice-card-cost">
                          Custo: {option.cost}$
                        </span>
                      )}
                    </button>
                  ))}
                </div>
              ) : (
                <p className="polis-not-your-turn">Aguarde sua vez para realizar uma ação.</p>
              )}
            </section>
            <button
              type="button"
              className="polis-choice-back"
              onClick={() => setSelectedTerritory(null)}
            >
              Voltar
            </button>
          </div>
        )}
        {pendingQuestion && (
          <QuestionPresentation
            question={pendingQuestion}
            targetName={pendingActionInfo?.territory_name}
            onAnswer={answerAttackQuestion}
          />
        )}

        {showQuestionPreview && (
          <QuestionPresentation
            key={previewQuestion?.question_id}
            question={previewQuestion}
            targetName="São Paulo"
            isDemo
            onAnswer={() => {}}
            onDismiss={() => setShowQuestionPreview(false)}
          />
        )}

        {showInitialDistribution && (
          <div className="polis-distribution-overlay" role="dialog" aria-modal="true" aria-label="Distribuição inicial de territórios">
            <section className="polis-distribution-panel">
              <img className="polis-distribution-art" src="/distribuicaosec.png" alt="Distribuição" />

              <div
                className="polis-distribution-state-card"
                style={{
                  backgroundColor: PARTY_COLORS[me?.party_id] ?? "#30C067",
                  display: distributionConfirmed ? "none" : "flex",
                }}
              >
                {myTerritories.length > 0 ? (
                  <>
                    <span className="polis-distribution-state-title">
                      {distributionTerritory?.name ?? "Selecione no mapa"}
                      {distributionTerritory?.region && (
                        <>
                          <br />
                          <span className="polis-distribution-region">
                            {distributionTerritory.region}
                          </span>
                        </>
                      )}
                    </span>
                    <div className="polis-distribution-controls" aria-label="Quantidade de influência">
                      <button
                        type="button"
                        className="polis-distribution-step"
                        onClick={() =>
                          setDistributionAmount(
                            Math.max(0, distributionAmountValue - 10)
                          )
                        }
                        aria-label="Diminuir influência em 10"
                      >
                        −
                      </button>
                      <input
                        className="polis-distribution-amount"
                        type="number"
                        min="0"
                        max={maxDistributionInfluence}
                        step="10"
                        value={distributionAmount === "" ? "" : distributionAmountValue}
                        onChange={(event) => {
                          const value = event.target.value;
                          setDistributionAmount(
                            value === ""
                              ? ""
                              : Math.min(
                                  maxDistributionInfluence,
                                  Math.max(0, Number(value) || 0)
                                )
                          );
                        }}
                        aria-label="Influência a distribuir"
                      />
                      <button
                        type="button"
                        className="polis-distribution-step"
                        onClick={() =>
                          setDistributionAmount(
                            Math.min(
                              maxDistributionInfluence,
                              distributionAmountValue + 10
                            )
                          )
                        }
                        aria-label="Aumentar influência em 10"
                      >
                        +
                      </button>
                      <button
                        type="button"
                        className="polis-distribution-confirm"
                        onClick={() => setDistributionConfirmed(true)}
                        aria-label="Confirmar distribuição"
                      >
                        <img src="/confirmar.png" alt="" />
                      </button>
                    </div>
                    <div className="polis-distribution-total">
                      Restante: {Math.max(
                        0,
                        maxDistributionInfluence - distributionAmountValue
                      )}
                    </div>
                  </>
                ) : (
                  <p className="polis-distribution-empty">Aguardando os territórios da partida…</p>
                )}
              </div>

              <div className="polis-distribution-map-wrap" aria-label="Mapa dos territórios da partida">
                <BrazilMapSvg
                  territories={territories}
                  players={players}
                  partyColors={PARTY_COLORS}
                  currentPlayerId={matchState?.your_player_id}
                  selectedTerritoryId={distributionTerritory?.territory_id ?? null}
                  selectableTerritoryIds={myTerritories.map((territory) => territory.territory_id)}
                  isActionable={true}
                  onSelectTerritory={(territory) => {
                    setDistributionTerritoryId(territory.territory_id);
                    setDistributionConfirmed(false);
                  }}
                  className="polis-distribution-map"
                />
              </div>

              <button
                type="button"
                className="polis-distribution-finish"
                onClick={() => setShowInitialDistribution(false)}
                disabled={!matchState || territories.length === 0 || !distributionTerritory}
                aria-label="Finalizar distribuição e começar a partida"
              >
                <img src="/finalizar.png" alt="" />
              </button>
            </section>
          </div>
        )}

        {!connected && (
          <div className="polis-connection-warning">
            Conectando à partida...
          </div>
        )}

        {gameNotice && (
          <div
            className="polis-game-notice-backdrop"
            aria-live="polite"
            aria-atomic="true"
          >
            <p
              key={gameNotice.id}
              className={`polis-game-notice polis-game-notice-${gameNotice.kind}`}
              role="status"
            >
              {gameNotice.message}
            </p>
          </div>
        )}

        {showVictoryScreen && (
          <div className="polis-victory-overlay" role="dialog" aria-modal="true" aria-label="Tela de vitória">
            <section className="polis-victory-screen">
              <img className="polis-victory-background" src="/fundovitoria.png" alt="" />
              <img className="polis-victory-title" src="/vencedor.png" alt="Vencedor" />

              <div className="polis-victory-winner-area">
                <div className="polis-victory-winner-card">
                  <img
                    className="polis-victory-winner-avatar"
                    src={getAvatarImage(victoryWinner?.avatar_id)}
                    alt={victoryWinner ? `Avatar de ${victoryWinner.username}` : ""}
                    onError={(event) => {
                      event.currentTarget.src = getAvatarImage("avatar_3");
                    }}
                  />
                  <img className="polis-victory-winner-podium" src="/podio.png" alt="" />
                  <div className="polis-victory-winner-label">
                    <span className="polis-victory-winner-name">
                      {victoryWinner?.username ?? "Aguardando jogadores"}
                    </span>
                    <span className="polis-victory-winner-count">
                      {victoryWinner?.controlledTerritories ?? 0} ⚑
                    </span>
                  </div>
                </div>
              </div>

              <section className="polis-victory-missions" aria-label="Colocação e missões dos jogadores">
                <img className="polis-victory-missions-art" src="/missoesrev.png" alt="Missões reveladas" />
                <div className="polis-victory-missions-list">
                  {victoryRanking.slice(1).map((rankedPlayer, index) => {
                    const mission = rankedPlayer.player_id === matchState?.your_player_id
                      ? matchState?.your_mission
                      : rankedPlayer.mission ?? rankedPlayer.secret_mission ??
                        matchState?.missions?.find((item) => item.owner_id === rankedPlayer.player_id)?.mission;
                    const missionText = mission
                      ? formatMission(mission, players)
                      : "Missão não disponível.";

                    return (
                      <div className="polis-victory-player" key={rankedPlayer.player_id}>
                        <span className="polis-victory-rank">{index + 2}º</span>
                        <div className="polis-victory-avatar-wrap">
                          <img
                            className="polis-victory-avatar"
                            src={getAvatarImage(rankedPlayer.avatar_id)}
                            alt={`Avatar de ${rankedPlayer.username}`}
                            onError={(event) => {
                              event.currentTarget.src = getAvatarImage("avatar_3");
                            }}
                          />
                          <span className="polis-victory-player-count">
                            {rankedPlayer.controlledTerritories} ⚑
                          </span>
                        </div>
                        <div className="polis-victory-player-info">
                          <span className="polis-victory-player-name">{rankedPlayer.username}</span>
                          <span className="polis-victory-mission-text">{missionText}</span>
                        </div>
                      </div>
                    );
                  })}
                  {victoryRanking.length <= 1 && (
                    <p className="polis-victory-empty">Ainda não há outros jogadores na partida.</p>
                  )}
                </div>
              </section>

              <button
                type="button"
                className="polis-victory-back"
                onClick={() => onReturnRoom()}
                aria-label="Voltar para a sala"
              >
                <img src="/voltarsala.png" alt="Voltar para a sala" />
              </button>
              <button
                type="button"
                className="polis-victory-exit"
                onClick={onLeaveRoom}
                aria-label="Sair da partida"
              >
                <img src="/sair2.png" alt="Sair" />
              </button>
            </section>
          </div>
        )}
      </main>


      <LastActionResult
        result={lastActionResult}
      />


    </div>
  );
}
