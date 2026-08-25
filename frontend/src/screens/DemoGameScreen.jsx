import { useEffect, useMemo, useRef, useState } from "react";

import BrazilMapSvg from "../components/BrazilMapSvg.jsx";

const PARTY_COLORS = {
  PR: "#E74C3C",
  PA: "#3498DB",
  PV: "#2ECC71",
  PD: "#F1C40F",
};

function formatMission(mission) {
  if (!mission) return "Missão não encontrada.";

  if (mission.type === "state") {
    return `Conquiste os territórios: ${mission.content.state.join(", ")}.`;
  }

  if (mission.type === "region") {
    return mission.content.region
      .map((item) => `Conquiste ${item.quantity} território(s) em ${item.region}`)
      .join(" + ");
  }

  if (mission.type === "destruction") {
    return `Destrua o jogador ${mission.content.destruction}. Se outro jogador destruí-lo antes, conquiste: ${mission.content.state.join(", ")}.`;
  }

  return "Tipo de missão desconhecido.";
}

function summarizeEvent(data) {
  if (!data?.payload) return data;

  return {
    type: data.type,
    current_turn_player_id: data.payload.current_turn_player_id,
    round: data.payload.round,
    status: data.payload.status,
    winner_id: data.payload.winner_id,
    last_action_result: data.payload.last_action_result,
  };
}

function getPlayerNameById(playerId, players) {
  const player = players.find((player) => player.player_id === playerId);

  return player ? `${player.username} (${player.player_id})` : playerId;
}

export default function DemoGameScreen() {
  const [matchId, setMatchId] = useState("");
  const [playerId, setPlayerId] = useState("p1");
  const [connected, setConnected] = useState(false);
  const [matchState, setMatchState] = useState(null);
  const [selectedTerritory, setSelectedTerritory] = useState(null);
  const [logs, setLogs] = useState([]);

  const [pendingQuestion, setPendingQuestion] = useState(null);
  const [pendingActionInfo, setPendingActionInfo] = useState(null);

  const wsRef = useRef(null);
  const winnerAlertShownRef = useRef(false);

  const players = matchState?.players ?? [];
  const territories = matchState?.territories ?? [];
  const attackOptions = matchState?.available_attack_options ?? [];

  const currentPlayer = useMemo(() => {
    if (!matchState) return null;

    return players.find(
      (player) => player.player_id === matchState.current_turn_player_id
    );
  }, [matchState, players]);

  const me = useMemo(() => {
    if (!matchState) return null;

    return players.find((player) => player.player_id === matchState.your_player_id);
  }, [matchState, players]);

  const isMyTurn =
    matchState &&
    matchState.status === "running" &&
    matchState.current_turn_player_id === matchState.your_player_id;

  function addLog(message, data = null) {
    setLogs((currentLogs) => [
      {
        id: crypto.randomUUID(),
        message,
        data,
        createdAt: new Date().toLocaleTimeString(),
      },
      ...currentLogs,
    ]);
  }

  function handleWinnerAlert(newMatchState) {
    if (
      newMatchState.status === "finished" &&
      newMatchState.winner_id &&
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
    if (!matchId.trim() || !playerId.trim()) {
      alert("Preencha match_id e player_id.");
      return;
    }

    if (wsRef.current) {
      wsRef.current.close();
    }

    winnerAlertShownRef.current = false;
    setPendingQuestion(null);
    setPendingActionInfo(null);

    const ws = new WebSocket(
      `ws://localhost:8000/ws/match/${matchId.trim()}/${playerId.trim()}`
    );

    wsRef.current = ws;

    ws.onopen = () => {
      setConnected(true);
      addLog(`Conectado como ${playerId} na partida ${matchId}`);
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);

      addLog(`Recebido evento: ${data.type ?? data.result?.type ?? "sem_tipo"}`, data);

      if (data.type === "attack_question") {
        setPendingQuestion(data.question);

        setPendingActionInfo({
          target_territory_id: data.target_territory_id,
          territory_id: data.territory_id,
          territory_name: data.territory_name,
          option_id: data.option_id,
          title: data.title,
          success_chance: data.success_chance,
        });

        return;
      }

      if (data.type === "match_state") {
        const newMatchState = data.payload;

        setMatchState(newMatchState);

        if (newMatchState?.last_action_result?.type === "attack_result") {
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
        alert(data.payload?.message ?? data.message ?? "Erro desconhecido.");
      }
    };

    ws.onerror = () => {
      addLog("Erro no WebSocket.");
    };

    ws.onclose = () => {
      setConnected(false);
      addLog("Conexão fechada.");
    };
  }

  function disconnect() {
    if (wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
    }

    setConnected(false);
    setPendingQuestion(null);
    setPendingActionInfo(null);
  }

  function sendAttack(optionId) {
    if (!wsRef.current || wsRef.current.readyState !== WebSocket.OPEN) {
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
        option_id: optionId,

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

    setSelectedTerritory(null);
  }

  function answerAttackQuestion(answer) {
  if (!wsRef.current || wsRef.current.readyState !== WebSocket.OPEN) {
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

  addLog(`Enviado answer_attack_question: ${answer ? "Verdadeiro" : "Falso"}`);

  setPendingQuestion(null);
  setPendingActionInfo(null);
}

  useEffect(() => {
    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, []);

  return (
    <main className="demo-game-page">
      <section className="demo-topbar">
        <div>
          <h1>Polis — Protótipo da Partida</h1>
          <p>Conexão direta na partida via WebSocket.</p>
        </div>

        <div className="demo-connect-panel">
          <label>
            Match ID
            <input
              value={matchId}
              onChange={(event) => setMatchId(event.target.value)}
              placeholder="ex: 39"
            />
          </label>

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

          <button onClick={connect}>
            {connected ? "Reconectar" : "Conectar"}
          </button>

          <button onClick={disconnect} disabled={!connected}>
            Desconectar
          </button>
        </div>
      </section>

      <section className="demo-layout">
        <aside className="demo-sidebar">
          <div className="demo-card">
            <h2>Você</h2>
            <p>
              <strong>Jogador:</strong>{" "}
              {me ? `${me.username} (${me.player_id})` : "Não conectado"}
            </p>
            <p>
              <strong>Partido:</strong> {me?.party_id ?? "-"}
            </p>
            <p>
              <strong>Status:</strong> {connected ? "Conectado" : "Desconectado"}
            </p>
          </div>

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
              <strong>Status da partida:</strong> {matchState?.status ?? "-"}
            </p>
            <p>
              <strong>Vencedor:</strong>{" "}
              {matchState?.winner_id
                ? getPlayerNameById(matchState.winner_id, players)
                : "Nenhum"}
            </p>
          </div>

          <div className="demo-card">
            <h2>Sua missão</h2>
            <p>{formatMission(matchState?.your_mission)}</p>
            <pre>{JSON.stringify(matchState?.your_mission ?? null, null, 2)}</pre>
          </div>

          <div className="demo-card">
            <h2>Território selecionado</h2>

            {selectedTerritory ? (
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

                  {attackOptions.length === 0 && (
                    <p>Nenhuma ação disponível.</p>
                  )}

                  {attackOptions.map((option) => (
                    <button
                      key={option.option_id}
                      className="demo-action-button"
                      onClick={() => sendAttack(option.option_id)}
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

                {!isMyTurn && (
                  <small>Você só pode agir quando for sua vez.</small>
                )}
              </>
            ) : (
              <p>Clique em um território no mapa.</p>
            )}
          </div>

          <div className="demo-card">
            <h2>Última ação</h2>

            {matchState?.last_action_result ? (
              <>
                <p>
                  <strong>Ação:</strong> {matchState.last_action_result.title}
                </p>
                <p>
                  <strong>Território:</strong>{" "}
                  {matchState.last_action_result.territory_name} (
                  {matchState.last_action_result.territory_id})
                </p>

                {matchState.last_action_result.question_was_correct !== undefined && (
                  <p>
                    <strong>Pergunta:</strong>{" "}
                    {matchState.last_action_result.question_was_correct
                      ? "Acertou"
                      : "Errou"}
                  </p>
                )}

                {matchState.last_action_result.base_success_chance !== undefined && (
                  <p>
                    <strong>Chance base:</strong>{" "}
                    {matchState.last_action_result.base_success_chance}%
                  </p>
                )}

                {matchState.last_action_result.adjusted_success_chance !== undefined && (
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

          <div className="demo-card">
            <h2>Jogadores</h2>

            <div className="demo-players">
              {players.map((player) => (
                <div key={player.player_id} className="demo-player">
                  <span
                    className="demo-color-dot"
                    style={{
                      backgroundColor: PARTY_COLORS[player.party_id] ?? "#999",
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

        <section className="demo-map-area">
          <BrazilMapSvg
            territories={territories}
            players={players}
            partyColors={PARTY_COLORS}
            selectedTerritoryId={selectedTerritory?.territory_id}
            onSelectTerritory={setSelectedTerritory}
            className="demo-map"
          />
        </section>

        <aside className="demo-log-panel">
          <h2>Log</h2>

          {logs.map((log) => (
            <div key={log.id} className="demo-log-item">
              <strong>
                [{log.createdAt}] {log.message}
              </strong>

              {log.data?.payload && (
                <pre>{JSON.stringify(summarizeEvent(log.data), null, 2)}</pre>
              )}

              {!log.data?.payload && log.data && (
                <pre>{JSON.stringify(log.data, null, 2)}</pre>
              )}
            </div>
          ))}
        </aside>
      </section>

      {pendingQuestion && (
        <div className="question-modal-backdrop">
          <div className="question-modal">
            <h2>Pergunta</h2>

            <p className="question-subject">{pendingQuestion.subject}</p>

            <p className="question-description">
              {pendingQuestion.description}
            </p>

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
              <button onClick={() => answerAttackQuestion(true)}>
                Verdadeiro
              </button>

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