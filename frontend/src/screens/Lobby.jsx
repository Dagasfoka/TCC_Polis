import { useEffect, useRef, useState } from "react";
import {
  getRoom,
  getPlayer,
  putReady,
  startRoom,
  deletePlayer,
  exitRoom,
  changeRoomPrivacy,
  getParties,
  chooseParty,
} from "../service/api.jsx";

const MAX_PLAYERS = 4;
const REFRESH_INTERVAL = 2000;

const FIXED_PARTIES = [
  { id: "1", name: "Vermelho", file: "/Vermelho.svg", colorHex: "#DA3A3C" },
  { id: "2", name: "Amarelo", file: "/Amarelo.svg", colorHex: "#E0A12A" },
  { id: "3", name: "Azul", file: "/Azul.svg", colorHex: "#28A3E0" },
  { id: "4", name: "Verde", file: "/Verde.svg", colorHex: "#30C067" },
];

export default function Lobby({
  player,
  room,
  onRoomUpdate,
  onLeave,
  onStart,
}) {
  const [currentRoom, setCurrentRoom] = useState(room);
  const [playerNames, setPlayerNames] = useState({});
  const [parties, setParties] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const roomCode = room.room_code;
  const playerId = player.player_id;

  const actionInProgress = useRef(false);
  const requestVersion = useRef(0);

  const callbacksRef = useRef({
    onRoomUpdate,
    onLeave,
    onStart,
  });

  useEffect(() => {
    callbacksRef.current = {
      onRoomUpdate,
      onLeave,
      onStart,
    };
  }, [onRoomUpdate, onLeave, onStart]);

  const players = currentRoom?.players ?? {};
  const playerEntries = Object.entries(players);
  const playerIds = Object.keys(players);
  const playerIdsKey = playerIds.join(",");

  const myRoomPlayer = players[playerId];

  const isHost = myRoomPlayer?.host === true;
  const isReady = myRoomPlayer?.ready === true;
  const isPrivate = currentRoom?.is_private === true;
  const myPartyId = myRoomPlayer?.party_id ?? null;

  const allReady =
    playerEntries.length === MAX_PLAYERS &&
    playerEntries.every(
      ([, roomPlayer]) =>
        roomPlayer.party_id &&
        (roomPlayer.host === true || roomPlayer.ready === true)
    );

  const emptySlots = Math.max(0, MAX_PLAYERS - playerEntries.length);

  function applyRoom(updatedRoom) {
    setCurrentRoom(updatedRoom);
    callbacksRef.current.onRoomUpdate(updatedRoom);
  }

  function processRoom(updatedRoom) {
    if (!updatedRoom) return;

    if (updatedRoom.status === "closed") {
      callbacksRef.current.onLeave();
      return;
    }

    if (!updatedRoom.players?.[playerId]) {
      console.warn(
        "Jogador ainda não apareceu na atualização da sala:",
        playerId,
        updatedRoom
      );
      return;
    }

    applyRoom(updatedRoom);

    if (updatedRoom.status === "in_game" && updatedRoom.match_id) {
      callbacksRef.current.onStart(updatedRoom.match_id);
    }
  }

  function handleChangePrivacy() {
    if (!isHost) return;

    runAction(async () => {
      const updatedRoom = await changeRoomPrivacy(
        roomCode,
        playerId,
        !isPrivate
      );
      processRoom(updatedRoom);
    });
  }

  useEffect(() => {
    let active = true;

    async function loadParties() {
      try {
        const data = await getParties();
        if (!active) return;
        setParties(data);
      } catch (err) {
        console.error("Não foi possível carregar os partidos:", err);
      }
    }

    loadParties();

    return () => {
      active = false;
    };
  }, []);

  useEffect(() => {
    let active = true;
    let timeoutId;

    async function refreshRoom() {
      if (!active) return;

      if (actionInProgress.current) {
        timeoutId = setTimeout(refreshRoom, REFRESH_INTERVAL);
        return;
      }

      const version = requestVersion.current;

      try {
        const updatedRoom = await getRoom(roomCode);

        if (!active || version !== requestVersion.current) return;

        processRoom(updatedRoom);
        setError("");
      } catch (err) {
        if (!active || version !== requestVersion.current) return;

        if (err.status === 404) {
          callbacksRef.current.onLeave();
          return;
        }

        setError("Não foi possível atualizar a sala.");
      } finally {
        if (active) {
          timeoutId = setTimeout(refreshRoom, REFRESH_INTERVAL);
        }
      }
    }

    refreshRoom();

    return () => {
      active = false;
      clearTimeout(timeoutId);
    };
  }, [roomCode, playerId]);

  useEffect(() => {
    let active = true;

    async function loadPlayerNames() {
      const ids = playerIdsKey ? playerIdsKey.split(",") : [];

      const results = await Promise.allSettled(
        ids.map(async (id) => {
          if (id === playerId) {
            return [id, player.username ?? player.nickname ?? id];
          }

          const playerData = await getPlayer(id);
          return [
            id,
            playerData.username ?? playerData.nickname ?? id,
          ];
        })
      );

      if (!active) return;

      const names = {};
      for (const result of results) {
        if (result.status === "fulfilled") {
          const [id, name] = result.value;
          names[id] = name;
        }
      }

      setPlayerNames(names);
    }

    loadPlayerNames();

    return () => {
      active = false;
    };
  }, [playerIdsKey, playerId, player.username, player.nickname]);

  async function runAction(action) {
    if (actionInProgress.current) return;

    actionInProgress.current = true;
    requestVersion.current += 1;

    setLoading(true);
    setError("");

    try {
      await action();
    } catch (err) {
      setError(err.message || "Não foi possível realizar a ação.");
    } finally {
      actionInProgress.current = false;
      setLoading(false);
    }
  }

  function handleChooseParty(partyId) {
    if (isReady) return;

    runAction(async () => {
      const updatedRoom = await chooseParty(roomCode, playerId, partyId);
      processRoom(updatedRoom);
    });
  }

  function handleReady() {
    if (isHost || isReady || !myPartyId) return;

    runAction(async () => {
      const updatedRoom = await putReady(roomCode, playerId);
      if (updatedRoom?.players) {
        processRoom(updatedRoom);
      } else {
        const refreshedRoom = await getRoom(roomCode);
        processRoom(refreshedRoom);
      }
    });
  }

  function handleKick(targetPlayerId) {
    if (!isHost || targetPlayerId === playerId) return;

    runAction(async () => {
      const updatedRoom = await deletePlayer(
        roomCode,
        playerId,
        targetPlayerId
      );

      if (updatedRoom?.players) {
        processRoom(updatedRoom);
      } else {
        const refreshedRoom = await getRoom(roomCode);
        processRoom(refreshedRoom);
      }
    });
  }

  function handleLeave() {
    runAction(async () => {
      await exitRoom(roomCode, playerId);
      callbacksRef.current.onLeave();
    });
  }

  function handleStart() {
    if (!isHost || !allReady) return;

    runAction(async () => {
      const match = await startRoom(roomCode, playerId);
      if (!match?.match_id) {
        throw new Error("O servidor não retornou o ID da partida.");
      }
      callbacksRef.current.onStart(match.match_id);
    });
  }

  const activePartiesList = FIXED_PARTIES.map((fixed, idx) => {
    const apiParty = parties[idx];
    return {
      id: apiParty?.id || fixed.id,
      name: apiParty?.name || fixed.name,
      file: fixed.file,
      colorHex: fixed.colorHex,
    };
  });

  return (
    <div className="lobby-body">
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;600;700;800&display=swap');

        * {
          box-sizing: border-box;
          margin: 0;
          padding: 0;
        }

        .lobby-body {
          font-family: 'Fira Code', monospace;
          background-color: #0d121d;
          background-image: url('/fundo.png');
          background-repeat: no-repeat;
          background-position: center center;
          background-size: cover;
          background-attachment: fixed;
          min-height: 100vh;
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          padding: 20px;
          color: #ffffff;
        }

        .header-bar-lobby {
          width: 100%;
          max-width: 1060px;
          display: flex;
          align-items: center;
          justify-content: center;
          position: relative;
          margin-bottom: 15px;
        }

        .header-logo {
          margin-bottom: 25px;
          display: flex;
          align-items: center;
          justify-content: center;
        }

        .header-logo img {
          height: 60px;
          width: auto;
          display: block;
        }

        .top-login-link-btn {
          position: absolute;
          right: 0;
          top: 50%;
          transform: translateY(-50%);
          background: none;
          border: none;
          color: #53f3c3;
          font-family: 'Fira Code', monospace;
          font-weight: 700;
          font-size: 16px;
          cursor: pointer;
        }

        .main-card {
          width: 100%;
          max-width: 1020px;
          height: 560px;
          position: relative;
          border-radius: 16px;
          overflow: hidden;
          box-shadow: 0 20px 50px rgba(0, 0, 0, 0.7);
          background-color: #1e2638;
          background-image: url('/lobby.png');
          background-size: cover;
          background-position: center;
          display: flex;
          align-items: center;
          justify-content: center;
          margin-top: -15px;
        }

        .room-content {
          position: relative;
          z-index: 2;
          width: 100%;
          height: 100%;
          display: flex;
          justify-content: space-between;
          align-items: flex-end;
          padding: 30px 45px 35px 45px;
        }

        /* PAINEL ESQUERDO: JOGADORES */
        .room-players-panel {
          position: relative;
          width: 440px;
          height: 480px;
          background-color: #d9d2c9;
          border: 3px solid #2b2b36;
          border-radius: 20px;
          padding: 45px 20px 20px 20px;
          display: flex;
          flex-direction: column;
          box-shadow: 0 10px 25px rgba(0,0,0,0.4);
        }

        .panel-banner-title {
          position: absolute;
          top: -30px;
          left: -15px;
          width: 270px;
          pointer-events: none;
          z-index: 10;
        }

        .panel-banner-title img {
          width: 100%;
          height: auto;
          filter: drop-shadow(0px 6px 10px rgba(0, 0, 0, 0.6));
        }

        .players-list-container {
          display: flex;
          flex-direction: column;
          gap: 14px;
          margin-top: 10px;
        }

        .player-slot-item {
          position: relative;
          width: 100%;
          height: 70px;
          display: flex;
          align-items: center;
        }

        .player-card-bar {
          position: absolute;
          width: 100%;
          height: 100%;
          border-radius: 35px 18px 18px 35px;
          border: 2px solid #1a1a24;
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 0 20px 0 80px;
          box-shadow: 0 4px 8px rgba(0, 0, 0, 0.25);
          transition: background-color 0.25s ease;
        }

        .player-avatar-circle {
          position: absolute;
          left: -2px;
          top: -2px;
          width: 74px;
          height: 74px;
          border-radius: 50%;
          z-index: 5;
          object-fit: cover;
          border: 3px solid #1a1a24;
          background-color: #2b334e;
        }

        .player-name-text {
          color: #ffffff;
          font-size: 1.2rem;
          font-weight: 800;
          text-shadow: 2px 2px 0px #000, -1px -1px 0px #000, 1px -1px 0px #000, -1px 1px 0px #000;
          z-index: 2;
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
          max-width: 200px;
        }

        .player-status-icon {
          z-index: 2;
          display: flex;
          align-items: center;
        }

        .crown-img {
          width: 22px;
          height: auto;
          display: block;
          object-fit: contain;
          filter: drop-shadow(0 2px 4px rgba(0,0,0,0.4));
        }

        .kick-btn-img {
          background: none;
          border: none;
          cursor: pointer;
          padding: 0;
          display: flex;
          align-items: center;
          justify-content: center;
          transition: transform 0.1s ease;
        }

        .kick-btn-img:hover:not(:disabled) {
          transform: scale(1.1);
        }

        .kick-btn-img img {
          height: 26px;
          width: auto;
          max-width: 26px;
          display: block;
          object-fit: contain;
        }

        .ready-check-img {
          position: absolute;
          right: -36px;
          width: 32px;
          height: auto;
          z-index: 5;
          filter: drop-shadow(0 2px 6px rgba(0,0,0,0.5));
        }

        .empty-slot-item {
          width: 100%;
          height: 70px;
          background-color: #ccc5b9;
          border: 2px solid #2b2b36;
          border-radius: 35px;
          display: flex;
          align-items: center;
          justify-content: center;
          color: #1a1a24;
          font-weight: 800;
          letter-spacing: 4px;
          font-size: 1.5rem;
        }

        /* PAINEL DIREITO */
        .room-actions-panel {
          width: 400px;
          height: 100%;
          display: flex;
          flex-direction: column;
          align-items: flex-end;
          justify-content: space-between;
        }

        .room-info-header {
          display: flex;
          align-items: center;
          gap: 12px;
          margin-top: 10px;
        }

        .code-badge {
          background-color: #000000;
          color: #ffffff;
          padding: 6px 16px;
          border-radius: 8px;
          text-align: center;
          box-shadow: 0 4px 10px rgba(0,0,0,0.4);
        }

        .code-badge span {
          display: block;
          font-size: 11px;
          color: #ffffff;
          font-weight: 700;
        }

        .code-badge strong {
          font-size: 1.3rem;
          letter-spacing: 2px;
        }

        .private-badge-btn {
          background: none;
          border: none;
          padding: 0;
          cursor: pointer;
        }

        .private-badge-img {
          height: 38px;
          width: auto;
          display: block;
          transition: transform 0.15s ease;
        }

        .private-badge-btn:hover:not(:disabled) .private-badge-img {
          transform: scale(1.05);
        }

        /* CARD DE PARTIDOS */
        .partidos-card-wrapper {
          position: relative;
          width: 340px;
          height: 160px;
          background-color: #d9d2c9;
          border: 3px solid #2b2b36;
          border-radius: 20px;
          padding: 18px 20px;
          display: flex;
          flex-direction: column;
          box-shadow: 0 10px 25px rgba(0,0,0,0.4);
        }

        .partidos-title-header {
          display: flex;
          align-items: center;
          margin-bottom: 16px;
        }

        .partidos-title-img {
          height: 36px;
          width: auto;
          display: block;
        }

        .partidos-grid-4 {
          display: grid;
          grid-template-columns: repeat(4, 1fr);
          gap: 12px;
          width: 100%;
          justify-items: center;
          align-items: center;
        }

        .color-party-btn {
          background: none;
          border: none;
          cursor: pointer;
          padding: 0;
          transition: transform 0.15s ease, opacity 0.15s ease;
          position: relative;
          display: flex;
          align-items: center;
          justify-content: center;
          width: 52px;
          height: 52px;
          border-radius: 50%;
        }

        .color-party-btn img.ball-img {
          width: 100%;
          height: 100%;
          display: block;
          object-fit: contain;
        }

        .color-party-btn.selected {
          box-shadow: inset 0 0 0 4px #ffffff;
        }

        .color-party-btn:hover:not(:disabled) {
          transform: scale(1.12);
        }

        .color-party-btn.occupied {
          opacity: 0.5;
          cursor: not-allowed;
        }

        .color-party-btn:disabled {
          cursor: not-allowed;
        }

        /* BOTÕES DE AÇÃO */
        .room-buttons-box {
          display: flex;
          flex-direction: column;
          align-items: flex-end;
          gap: 10px;
          width: 100%;
        }

        .btn-action-img {
          background: none;
          border: none;
          cursor: pointer;
          transition: transform 0.15s ease;
          padding: 0;
          display: block;
        }

        .btn-action-img:hover:not(:disabled) {
          transform: scale(1.04);
        }

        .btn-action-img:disabled {
          opacity: 0.5;
          cursor: not-allowed;
        }

        .btn-action-img.btn-pronto img {
          width: 320px;
          height: auto;
          display: block;
          filter: drop-shadow(0px 8px 16px rgba(0, 0, 0, 0.5));
        }

        .btn-action-img.btn-sair img {
          width: 170px;
          height: auto;
          display: block;
          filter: drop-shadow(0px 6px 12px rgba(0, 0, 0, 0.5));
        }

        .status-error-msg {
          color: #ff5252;
          font-size: 13px;
          font-weight: 700;
          text-align: right;
          margin-top: 4px;
        }
      `}</style>

      {/* Topo */}
      <div className="header-bar-lobby">
        <div className="header-logo">
          <img src="/polis.png" alt="Logo Polis" />
        </div>
      </div>

      {/* Card Principal */}
      <div className="main-card">
        <div className="room-content">
          {/* PAINEL ESQUERDO: JOGADORES */}
          <div className="room-players-panel">
            <div className="panel-banner-title">
              <img src="/titulolobby.png" alt="JOGADORES" />
            </div>

            <div className="players-list-container">
              {playerEntries.map(([id, roomPlayer]) => {
                const selectedParty = activePartiesList.find(
                  (p) => String(p.id) === String(roomPlayer.party_id)
                );
                const isMe = id === playerId;
                const pName = playerNames[id] ?? id;
                const bgColor = selectedParty?.colorHex || "#2b334e";

                return (
                  <div className="player-slot-item" key={id}>
                    <img
                      src="/avatarsapo.png"
                      className="player-avatar-circle"
                      alt={pName}
                    />

                    <div
                      className="player-card-bar"
                      style={{ backgroundColor: bgColor }}
                    >
                      <span className="player-name-text">
                        {pName} {isMe ? "(você)" : ""}
                      </span>

                      <div className="player-status-icon">
                        {roomPlayer.host ? (
                          <img
                            src="/coroa.png"
                            className="crown-img"
                            alt="Líder"
                          />
                        ) : (
                          isHost && (
                            <button
                              className="kick-btn-img"
                              onClick={() => handleKick(id)}
                              disabled={loading}
                              title="Expulsar"
                            >
                              <img src="/expulsar.png" alt="Expulsar" />
                            </button>
                          )
                        )}
                      </div>
                    </div>

                    {(roomPlayer.ready || roomPlayer.host) && (
                      <img
                        src="/vpronto.png"
                        className="ready-check-img"
                        alt="Pronto"
                      />
                    )}
                  </div>
                );
              })}

              {Array.from({ length: emptySlots }).map((_, i) => (
                <div className="empty-slot-item" key={`empty-${i}`}>
                  ...
                </div>
              ))}
            </div>
          </div>

          {/* PAINEL DIREITO */}
          <div className="room-actions-panel">
            <div className="room-info-header">
              <div className="code-badge">
                <span>Código</span>
                <strong>{roomCode}</strong>
              </div>

              {/* Botão de Privacidade */}
              <button
                type="button"
                className="private-badge-btn"
                onClick={handleChangePrivacy}
                disabled={loading || !isHost}
                title={
                  isHost
                    ? "Alternar privacidade da sala"
                    : "Apenas o host pode alterar a privacidade"
                }
              >
                <img
                  src={isPrivate ? "/PRIVACIDADE.png" : "/publica.png"}
                  alt={isPrivate ? "Privada" : "Pública"}
                  className="private-badge-img"
                />
              </button>
            </div>

            {/* Card de Escolha de Partidos */}
            <div className="partidos-card-wrapper">
              <div className="partidos-title-header">
                <img
                  src="/Partidos.png"
                  alt="Partidos"
                  className="partidos-title-img"
                />
              </div>

              <div className="partidos-grid-4">
                {activePartiesList.map((party) => {
                  const isSelected = String(myPartyId) === String(party.id);
                  const usedByOther = playerEntries.some(
                    ([id, rp]) =>
                      id !== playerId &&
                      String(rp.party_id) === String(party.id)
                  );

                  return (
                    <button
                      key={party.id}
                      type="button"
                      className={`color-party-btn ${
                        isSelected ? "selected" : ""
                      } ${usedByOther ? "occupied" : ""}`}
                      onClick={() => handleChooseParty(party.id)}
                      disabled={loading || isReady || usedByOther}
                      title={`${party.name}${
                        usedByOther ? " (Ocupado por outro jogador)" : ""
                      }`}
                    >
                      <img
                        src={party.file}
                        alt={party.name}
                        className="ball-img"
                      />
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Botões de Ação */}
            <div className="room-buttons-box">
              {isHost ? (
                <button
                  type="button"
                  className="btn-action-img btn-pronto"
                  onClick={handleStart}
                  disabled={loading || !allReady}
                  title={
                    !allReady
                      ? "Aguarde todos os jogadores estarem prontos"
                      : "Iniciar Partida"
                  }
                >
                  <img src="/PRONTO.png" alt="Iniciar Partida" />
                </button>
              ) : (
                <button
                  type="button"
                  className="btn-action-img btn-pronto"
                  onClick={handleReady}
                  disabled={loading || isReady || !myPartyId}
                  title={
                    !myPartyId
                      ? "Escolha um partido primeiro"
                      : isReady
                      ? "Você já está pronto"
                      : "Marcar como Pronto"
                  }
                >
                  <img src="/PRONTO.png" alt="Estou Pronto" />
                </button>
              )}

              <button
                type="button"
                className="btn-action-img btn-sair"
                onClick={handleLeave}
                disabled={loading}
              >
                <img src="/sairlobby.png" alt="Sair" />
              </button>
            </div>

            {error && <p className="status-error-msg">{error}</p>}
          </div>
        </div>
      </div>
    </div>
  );
}