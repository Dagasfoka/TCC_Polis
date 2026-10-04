import { useEffect, useMemo, useRef, useState } from "react";

import BrazilMapSvg from "../components/BrazilMapSvg.jsx";

const PARTY_COLORS = {
  PR: "#E74C3C",
  PA: "#3498DB",
  PV: "#2ECC71",
  PD: "#F1C40F",
};

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

  const influence = Number(player.match_influence ?? 0);

  return (
    <div
      className={[
        "polis-player-card",
        isCurrentTurn ? "polis-player-current" : "",
        isMe ? "polis-player-me" : "",
      ]
        .filter(Boolean)
        .join(" ")}
      style={{ "--party-color": partyColor }}
    >
      {isNext && <div className="polis-next-label">Próximo</div>}

      {isMe && <div className="polis-you-label">Você</div>}

      <div className="polis-player-main">
        <div className="polis-player-avatar">{initials}</div>

        <div className="polis-player-stats">
          <div className="polis-stat-row">
            <span className="polis-stat-icon">◆</span>

            <div className="polis-stat-track polis-influence-track">
              <div
                className="polis-stat-fill"
                style={{
                  width: `${Math.max(0, Math.min(influence, 100))}%`,
                }}
              />
              <strong>{player.match_influence ?? 0}%</strong>
            </div>
          </div>

          <div className="polis-stat-row">
            <span className="polis-stat-icon">$</span>

            <div className="polis-stat-track polis-money-track">
              <strong>{player.match_money ?? 0}$</strong>
            </div>
          </div>

          <div className="polis-stat-row">
            <span className="polis-stat-icon">●</span>

            <div className="polis-stat-track polis-corruption-track">
              <strong>{player.match_corruption ?? 0}</strong>
            </div>
          </div>
        </div>
      </div>

      <div className="polis-player-name">{player.username}</div>
    </div>
  );
}

export default function DemoGameScreen({
  initialMatchId,
  initialPlayerId,
  onMatchNotFound,
}) {
  const matchId = String(initialMatchId ?? "");
  const playerId = initialPlayerId ?? "";

  const [connected, setConnected] = useState(false);
  const [matchState, setMatchState] = useState(null);
  const [selectedTerritory, setSelectedTerritory] = useState(null);
  const [availableActions, setAvailableActions] = useState([]);
  const [actionType, setActionType] = useState(null);

  const [pendingQuestion, setPendingQuestion] = useState(null);
  const [pendingActionInfo, setPendingActionInfo] = useState(null);

  const wsRef = useRef(null);
  const winnerAlertShownRef = useRef(false);
  const reconnectTimerRef = useRef(null);
  const shouldReconnectRef = useRef(true);
  const isUnmountingRef = useRef(false);

  const players = matchState?.players ?? [];
  const territories = matchState?.territories ?? [];

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

      alert(`Fim de jogo! Vencedor: ${winnerName}`);
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

        setMatchState(newMatchState);

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

        setMatchState(newMatchState);

        setPendingQuestion(null);
        setPendingActionInfo(null);

        handleWinnerAlert(newMatchState);

        return;
      }

      if (data.match && data.result) {
        const newMatchState = data.match;

        setMatchState(newMatchState);

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
        onMatchNotFound(message)

        alert(message);

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

    wsRef.current.send(
      JSON.stringify({
        type: "choose_attack_option",

        target_territory_id: selectedTerritory.territory_id,
        territory_id: selectedTerritory.territory_id,
        action_id: optionId,
        action_type:action_type,

        payload: {
          target_territory_id: selectedTerritory.territory_id,
          territory_id: selectedTerritory.territory_id,
          action_id: optionId,
          action_type:action_type,
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
        />
      </div>

      <section className="polis-map-container">
        <BrazilMapSvg
          territories={territories}
          players={players}
          partyColors={PARTY_COLORS}
          selectedTerritoryId={
            selectedTerritory?.territory_id
          }
          onSelectTerritory={handleTerritorySelection}
          className="polis-main-map"
        />
      </section>

      <aside className="polis-mission-card polis-mission-right">
        <div className="polis-mission-heading">
          <span>Sua missão</span>

          {me?.party_id && (
            <span
              className="polis-mission-party"
              style={{
                backgroundColor:
                  PARTY_COLORS[me.party_id] ?? "#7f8c8d",
              }}
            >
              {me.party_id}
            </span>
          )}
        </div>

        <p>{missionText}</p>
      </aside>

      {selectedTerritory && (
        <div className="polis-territory-popup polis-territory-left">
          <button
            type="button"
            className="polis-close-popup"
            onClick={() => setSelectedTerritory(null)}
            aria-label="Fechar"
          >
            ×
          </button>

          <h2>
            {selectedTerritory.name ??
              selectedTerritory.territory_id}
          </h2>

          <div className="polis-territory-info">
            <span>
              Região
              <strong>
                {selectedTerritory.region ?? "-"}
              </strong>
            </span>

            <span>
              Influência
              <strong>
                {selectedTerritory.current_influence ?? 0}
              </strong>
            </span>
          </div>

          {isMyTurn ? (
            <>
              <h3>
                {actionType === "attack"
                  ? "Ações de Ataque"
                  : "Ações de Defesa"}
              </h3>

              <div className="polis-attack-actions">
                {attackOptions.length === 0 && (
                  <p>Nenhuma ação disponível.</p>
                )}

                {availableActions.map((option) => (
                  <button
                    type="button"
                    key={option.action_id}
                    onClick={() =>
                      sendAttack(option.action_id, option.action_type)
                    }
                  >
                    <strong>{option.title}</strong>

                    {option.influence_generated !==
                      undefined && (
                        <span>
                          +
                          {option.influence_generated} influência
                        </span>
                      )}

                    {option.success_chance !== undefined && (
                      <small>
                        {option.success_chance}% de sucesso
                      </small>
                    )}

                    {option.description && (
                      <small>{option.description}</small>
                    )}
                  </button>
                ))}
              </div>
            </>
          ) : (
            <p className="polis-not-your-turn">
              Aguarde sua vez para realizar uma ação.
            </p>
          )}
        </div>
      )}

      {pendingQuestion && (
        <div className="question-modal-backdrop">
          <div className="question-modal polis-question-modal">
            <h2>
              {pendingQuestion.subject ?? "Pergunta"}
            </h2>

            {pendingActionInfo?.territory_name && (
              <p className="polis-question-territory">
                Ação em{" "}
                <strong>
                  {pendingActionInfo.territory_name}
                </strong>
              </p>
            )}

            <p className="question-description">
              {pendingQuestion.description}
            </p>

            <div className="question-buttons">
              {Object.entries(
                pendingQuestion?.options ?? {}
              ).map(([letter, text]) => (
                <button
                  type="button"
                  key={letter}
                  onClick={() =>
                    answerAttackQuestion(letter)
                  }
                >
                  <strong>{letter}</strong>
                  <span>{text}</span>
                </button>
              ))}
            </div>
          </div>
        </div>
      )}

      {!connected && (
        <div className="polis-connection-warning">
          Conectando à partida...
        </div>
      )}
    </main>
  );
}
