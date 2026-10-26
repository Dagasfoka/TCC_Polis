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
import { getAvatarPortraitImage } from "../utils/avatarAssets.js";

const MAX_PLAYERS = 4;
const REFRESH_INTERVAL = 2000;

const PARTY_COLORS = {
  PR: "#DA3A3C",
  PD: "#E0A12A",
  PA: "#28A3E0",
  PV: "#30C067",
};

export default function Lobby({
  player,
  room,
  onRoomUpdate,
  onLeave,
  onStart,
}) {
  const [currentRoom, setCurrentRoom] = useState(room);
  const [playerInfos, setPlayerInfos] = useState({});
  const [parties, setParties] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [isRoomCodeVisible, setIsRoomCodeVisible] = useState(true);
  const [roomCodeCopied, setRoomCodeCopied] = useState(false);

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

  async function handleCopyRoomCode() {
    try {
      await navigator.clipboard.writeText(String(roomCode));
      setRoomCodeCopied(true);
      window.setTimeout(() => setRoomCodeCopied(false), 1500);
    } catch {
      setError("Não foi possível copiar o código da sala.");
    }
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

    async function loadPlayerInfos() {
      const ids = playerIdsKey
        ? playerIdsKey.split(",")
        : [];

      const results = await Promise.allSettled(
        ids.map(async (id) => {
          const playerData = await getPlayer(id);
          console.log("PLAYER DO LOBBY:", id, playerData);

          return [
            id,
            {
              username:
                playerData.username ??
                playerData.nickname ??
                id,

              avatar_id:
                playerData.avatar_id ?? null,
            },
          ];
        })
      );

      if (!active) return;

      const infos = {};

      for (const result of results) {
        if (result.status === "fulfilled") {
          const [id, info] = result.value;
          infos[id] = info;
        }
      }

      setPlayerInfos(infos);
    }

    loadPlayerInfos();

    return () => {
      active = false;
    };
  }, [playerIdsKey]);

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
    if (isHost || !myPartyId) return;

    runAction(async () => {
      const updatedRoom = await putReady(
        roomCode,
        playerId
      );

      if (updatedRoom?.players) {
        processRoom(updatedRoom);
      } else {
        const refreshedRoom =
          await getRoom(roomCode);

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

const activePartiesList = parties.map((party) => ({
  id: party.id,
  name: party.name,
  colorHex:
    PARTY_COLORS[String(party.id).toUpperCase()] || party.color || "#ffffff",
}));

  return (
    <div className="lobby-body">
      <svg aria-hidden="true" width="0" height="0" style={{ position: "absolute" }}>
        <defs>
          <filter id="room-lock-green" colorInterpolationFilters="sRGB">
            <feColorMatrix type="matrix" values="0.08 0 0 0 0  0 0.82 0 0 0  0 0 0.22 0 0  0 0 0 1 0" />
          </filter>
          <filter id="room-lock-red" colorInterpolationFilters="sRGB">
            <feColorMatrix type="matrix" values="0.9 0 0 0 0  0 0.12 0 0 0  0 0 0.12 0 0  0 0 0 1 0" />
          </filter>
        </defs>
      </svg>
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
          max-width: 1020px;
          height: 60px;
          display: flex;
          align-items: center;
          justify-content: center;
          position: relative;
          margin-bottom: 22px;
        }

        .header-logo {
          display: flex;
          align-items: center;
          justify-content: center;
        }

        .header-logo img {
          height: 60px;
          width: auto;
          display: block;
        }

        .lobby-exit-btn {
          position: absolute;
          right: 0;
          top: calc(50% + 20px);
          transform: translateY(-50%);
          background: transparent;
          border: none;
          padding: 0;
          color: #ffffff;
          font-family: "Coolvetica", sans-serif;
          font-size: 26.4px;
          font-weight: 400;
          cursor: pointer;
        }

        .main-card {
          width: 100%;
          max-width: 1020px;
          height: 560px;
          position: relative;
          border-radius: 16px;
          overflow: visible;
          box-shadow: 0 20px 50px rgba(0, 0, 0, 0.7);
          background-color: #1e2638;
          background-image: url('/fundolobby.png');
          background-size: cover;
          background-position: center;
          display: flex;
          align-items: center;
          justify-content: center;
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
          overflow: visible;
          width: 480px;
          height: 448px;
          transform: translateY(8px);
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
          left: -25px;
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
          overflow: visible;
          gap: 14px;
          margin-top: 10px;
          padding-right: 40px;
        }

        .player-slot-item {
          position: relative;
          overflow: visible;
          width: 100%;
          height: 78px;
          display: flex;
          align-items: center;
        }

        .player-card-bar {
          position: absolute;
          overflow: visible;
          top: -2px;
          width: 100%;
          height: calc(100% + 4px);
          border-radius: 39px;
          border: none;
          outline: none;
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 0 20px 0 88px;
          box-shadow: 0 4px 0 color-mix(in srgb, var(--party-color) 72%, #000000);
          transition: background-color 0.25s ease, border-color 0.25s ease;
        }

        .player-avatar-circle {
          position: absolute;
          left: 6px;
          top: 2px;
          width: 74px;
          height: 74px;
          border-radius: 50%;
          z-index: 5;
          object-fit: cover;
          border: 3px solid #000000;
          box-sizing: border-box;
          background-color: #2b334e;
          transition: border-color 0.25s ease;
        }

        .player-name-text {
          display: inline-block;
          font-family: "Coolvetica", sans-serif;
          flex-shrink: 0;
          line-height: 1.4;
          padding: 6px;
          margin: -6px;
          color: #ffffff;
          font-size: 1.4rem;
          font-weight: 400;
          font-synthesis: none;
          -webkit-text-stroke: 5px #000;
          paint-order: stroke fill;
          text-shadow:
            2px 2px 0 #000,
            3px 2px 0 #000,
            2px 3px 0 #000,
            3px 3px 0 #000;
          z-index: 2;
          white-space: nowrap;
          overflow: visible;
          text-overflow: clip;
          max-width: none;
        }

        .player-status-icon {
          z-index: 2;
          display: flex;
          align-items: center;
        }

        .crown-img {
          width: 30px;
          height: auto;
          display: block;
          object-fit: contain;
          filter: none;
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
          filter: none;
        }

        .empty-slot-item {
          width: 100%;
          height: 82px;
          box-sizing: border-box;
          background: rgba(255,255,255,0.22);
          border: 1px dashed rgba(42, 48, 64, 0.62);
          border-radius: 39px;
          display: flex;
          align-items: center;
          justify-content: center;
          color: #67645f;
          font-weight: 600;
          letter-spacing: 0.02em;
          font-size: 0.9rem;
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
          position: absolute;
          top: 50px;
          right: 0;
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 24px;
          margin-top: 0;
          z-index: 4;
        }

        .code-badge {
          position: relative;
          width: 310px;
          height: 120px;
          transform: scale(1.65);
          transform-origin: right center;
          overflow: hidden;
          display: flex;
          align-items: center;
          justify-content: flex-start;
          color: #ffffff;
          padding: 0;
          border: 0;
          border-radius: 0;
          background: transparent;
          text-align: center;
          box-shadow: none;
        }

        .code-badge-art {
          position: absolute;
          top: -50px;
          left: 15px;
          width: 295px;
          height: auto;
          display: block;
          pointer-events: none;
          z-index: 0;
        }

        .code-badge strong {
          position: absolute;
          left: 42px;
          top: 50px;
          min-width: 156px;
          padding: 3px 8px;
          color: #ffffff;
          font-size: 24px;
          line-height: 1.15;
          letter-spacing: 2px;
          z-index: 1;
        }

        .code-lock-toggle {
          position: absolute;
          top: calc(50% - 9px);
          right: 45px;
          width: 36px;
          height: 36px;
          display: flex;
          align-items: flex-end;
          justify-content: center;
          padding: 0;
          border: 0;
          background: transparent;
          cursor: pointer;
          z-index: 2;
          transform: translateY(-50%);
        }

        .code-lock-art {
          width: 27px;
          height: auto;
          object-fit: contain;
          pointer-events: none;
        }

        .room-code-control {
          position: absolute;
          z-index: 2;
          width: 36px;
          height: 36px;
          display: inline-flex;
          align-items: center;
          justify-content: center;
          padding: 0;
          border: 0;
          border-radius: 0;
          background: transparent;
          color: #ffffff;
          font-size: 18px;
          line-height: 1;
          cursor: pointer;
        }

        .room-code-control:hover {
          transform: none;
        }

        .room-code-control img {
          position: absolute;
          top: 50%;
          left: 50%;
          width: 30px;
          height: 30px;
          object-fit: contain;
          display: block;
          transform: translate(-50%, -50%);
          transition: opacity 0.18s ease;
        }

        .room-code-copy .copy-confirmation-icon {
          width: 24px;
          height: 24px;
          filter: brightness(0) invert(1);
          opacity: 0;
        }

        .room-code-copy.is-copied .copy-icon {
          opacity: 0;
        }

        .room-code-copy.is-copied .copy-confirmation-icon {
          opacity: 1;
        }

        .room-code-eye {
          right: 92px;
          bottom: 28px;
        }

        .room-code-copy {
          right: 92px;
          top: 22px;
        }

        /* CARD DE PARTIDOS */
        .partidos-card-wrapper {
          position: relative;
          z-index: 3;
          top: 184px;
          width: 370px;
          height: 148px;
          transform: translateX(-25px) scale(1.1);
          transform-origin: left center;
          background: transparent;
          border: 0;
          border-radius: 0;
          padding: 0;
          display: flex;
          flex-direction: column;
          box-shadow: none;
        }

        .partidos-card-art {
          position: absolute;
          top: -15px;
          left: 0;
          width: 370px;
          height: auto;
          display: block;
          pointer-events: none;
          z-index: 0;
        }

        .partidos-grid-4 {
          position: absolute;
          z-index: 1;
          left: 49px;
          right: auto;
          bottom: 40px;
          transform: rotate(-5deg);
          transform-origin: center center;
          display: grid;
          grid-template-columns: repeat(4, 1fr);
          gap: 0;
          width: 290px;
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
          width: 48px;
          height: 48px;
          border-radius: 50%;
        }

        .color-party-btn.selected {
          outline: 3px solid #ffffff;
          outline-offset: 2px;
          transform: scale(1.08);
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
          position: relative;
          z-index: 3;
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
          width: 350px;
          height: auto;
          display: block;
          object-fit: contain;
        }

        .btn-action-img.btn-pronto {
          width: auto;
          height: auto;
          background: transparent;
          clip-path: none;
          filter: none;
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
        <button
          type="button"
          className="lobby-exit-btn"
          onClick={handleLeave}
          disabled={loading}
          title="Sair do lobby"
        >
          Sair
        </button>
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
                const playerInfo = playerInfos[id];

                const pName =
                  playerInfo?.username ?? id;

                const avatarId =
                  playerInfo?.avatar_id ?? null;
                const bgColor = String(roomPlayer.party_id) === "PD"
                  ? "#E0A12A"
                  : selectedParty?.colorHex || "#2b334e";

                return (
                  <div className="player-slot-item" key={id}>

                    <img
                      src={getAvatarPortraitImage(avatarId)}
                      className="player-avatar-circle"
                      alt={pName}
                      style={{ "--party-color": bgColor }}
                    />

                    <div
                      className="player-card-bar"
                      style={{ backgroundColor: bgColor, "--party-color": bgColor }}
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
                              <img
                                src="/expulsar.png"
                                alt="Expulsar"
                              />
                            </button>
                          )
                        )}
                      </div>
                    </div>

                    {(roomPlayer.ready || (roomPlayer.host && roomPlayer.party_id)) && (
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
                  Aguardando jogador
                </div>
              ))}
            </div>
          </div>

          {/* PAINEL DIREITO */}
          <div className="room-actions-panel">
            <div className="room-info-header">
              <div className="code-badge">
                <img src="/codigolobby.png" alt="" className="code-badge-art" />
                <strong>{isRoomCodeVisible ? roomCode : "••••••"}</strong>
                <button
                  type="button"
                  className="code-lock-toggle"
                  onClick={handleChangePrivacy}
                  disabled={loading || !isHost}
                  aria-label={isPrivate ? "Tornar sala pública" : "Tornar sala privada"}
                  title={isPrivate ? "Tornar sala pública" : "Tornar sala privada"}
                >
                  <img
                    src={isPrivate ? "/closelock.png" : "/openlock.png"}
                    alt=""
                    className="code-lock-art"
                    style={{ filter: isPrivate ? "url(#room-lock-red)" : "url(#room-lock-green)" }}
                  />
                </button>
                <button
                  type="button"
                  className="room-code-control room-code-eye"
                  onClick={() => setIsRoomCodeVisible((visible) => !visible)}
                  aria-label={isRoomCodeVisible ? "Esconder código da sala" : "Mostrar código da sala"}
                  title={isRoomCodeVisible ? "Esconder código" : "Mostrar código"}
                >
                  <img src="/OLHO.png" alt="" />
                </button>
                <button
                  type="button"
                  className={`room-code-control room-code-copy ${roomCodeCopied ? "is-copied" : ""}`}
                  onClick={handleCopyRoomCode}
                  aria-label={roomCodeCopied ? "Código copiado" : "Copiar código da sala"}
                  title={roomCodeCopied ? "Copiado!" : "Copiar código"}
                >
                  <img src="/COPIAR.png" alt="" className="copy-icon" />
                  <img src="/vpronto.png" alt="" className="copy-confirmation-icon" />
                </button>
              </div>

            </div>

            {/* Card de Escolha de Partidos */}
            <div className="partidos-card-wrapper">
              <img src="/partidoslobby.png" alt="" className="partidos-card-art" />

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
                      className={`color-party-btn ${isSelected ? "selected" : ""
                        } ${usedByOther ? "occupied" : ""}`}
                      onClick={() => handleChooseParty(party.id)}
                      disabled={loading || isReady || usedByOther}
                      aria-pressed={isSelected}
                      style={{ backgroundColor: party.colorHex }}
                      title={`${party.name}${usedByOther ? " (Ocupado por outro jogador)" : ""
                        }`}
                    >
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
                  <img src="/COMEÇAR.png" alt="Começar partida" />
                </button>
              ) : (
                <button
                  type="button"
                  className="btn-action-img btn-pronto"
                  onClick={handleReady}
                  disabled={loading || !myPartyId}
                  title={
                    !myPartyId
                      ? "Escolha um partido primeiro"
                      : isReady
                        ? "Retirar pronto"
                        : "Marcar como pronto"
                  }
                  aria-pressed={isReady}
                >
                  <img
                    src={isReady ? "/CANCELAR.png" : "/Pronto.png"}
                    alt={isReady ? "Cancelar pronto" : "Estou Pronto"}
                  />
                </button>
              )}

            </div>

            {error && <p className="status-error-msg">{error}</p>}
          </div>
        </div>
      </div>
    </div>
  );
}
