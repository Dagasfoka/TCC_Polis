
import { useEffect, useRef, useState } from "react";

import {
  getRoom,
  getPlayer,
  putReady,
  startRoom,
  deletePlayer,
  exitRoom,
} from "../services/api.js";

const MAX_PLAYERS = 4;
const REFRESH_INTERVAL = 2000;

export default function Lobby({
  player,
  room,
  onRoomUpdate,
  onLeave,
  onStart,
}) {
  const [currentRoom, setCurrentRoom] = useState(room);
  const [playerNames, setPlayerNames] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const roomCode = room.room_code;
  const playerId = player.player_id;

  // Evita que uma consulta antiga sobrescreva uma ação recente.
  const actionInProgress = useRef(false);
  const requestVersion = useRef(0);

  // Mantém os callbacks atualizados sem reiniciar o polling.
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

  const allReady =
    playerEntries.length === MAX_PLAYERS &&
    playerEntries.every(
      ([, roomPlayer]) =>
        roomPlayer.host === true ||
        roomPlayer.ready === true
    );

  const emptySlots = Math.max(
    0,
    MAX_PLAYERS - playerEntries.length
  );

  function applyRoom(updatedRoom) {
    setCurrentRoom(updatedRoom);
    callbacksRef.current.onRoomUpdate(updatedRoom);
  }

  function processRoom(updatedRoom) {
    // Jogador expulso, sala encerrada ou sala inexistente.
    if (
      !updatedRoom ||
      updatedRoom.status === "closed" ||
      !updatedRoom.players?.[playerId]
    ) {
      callbacksRef.current.onLeave();
      return;
    }

    applyRoom(updatedRoom);

    // Todos entram na mesma partida quando ela começar.
    if (
      updatedRoom.status === "in_game" &&
      updatedRoom.match_id
    ) {
      callbacksRef.current.onStart(updatedRoom.match_id);
    }
  }

  // Atualização automática da sala.
  useEffect(() => {
    let active = true;
    let timeoutId;

    async function refreshRoom() {
      if (!active) return;

      // Não consulta enquanto uma ação do jogador está em andamento.
      if (actionInProgress.current) {
        timeoutId = setTimeout(
          refreshRoom,
          REFRESH_INTERVAL
        );
        return;
      }

      const version = requestVersion.current;

      try {
        const updatedRoom = await getRoom(roomCode);

        if (!active || version !== requestVersion.current) {
          return;
        }

        processRoom(updatedRoom);
        setError("");
      } catch (err) {
        if (!active || version !== requestVersion.current) {
          return;
        }

        if (err.status === 404) {
          callbacksRef.current.onLeave();
          return;
        }

        setError("Não foi possível atualizar a sala.");
      } finally {
        if (active) {
          timeoutId = setTimeout(
            refreshRoom,
            REFRESH_INTERVAL
          );
        }
      }
    }

    refreshRoom();

    return () => {
      active = false;
      clearTimeout(timeoutId);
    };
  }, [roomCode, playerId]);

  // Busca os nicknames quando alguém entra ou sai da sala.
  useEffect(() => {
    let active = true;

    async function loadPlayerNames() {
      const ids = playerIdsKey
        ? playerIdsKey.split(",")
        : [];

      const results = await Promise.allSettled(
        ids.map(async (id) => {
          if (id === playerId) {
            return [
              id,
              player.username ?? player.nickname ?? id,
            ];
          }

          const playerData = await getPlayer(id);

          return [
            id,
            playerData.username ??
              playerData.nickname ??
              id,
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
  }, [
    playerIdsKey,
    playerId,
    player.username,
    player.nickname,
  ]);

  // Centraliza o controle das ações do lobby.
  async function runAction(action) {
    if (actionInProgress.current) return;

    actionInProgress.current = true;
    requestVersion.current += 1;

    setLoading(true);
    setError("");

    try {
      await action();
    } catch (err) {
      setError(
        err.message || "Não foi possível realizar a ação."
      );
    } finally {
      actionInProgress.current = false;
      setLoading(false);
    }
  }

  // Jogador marca pronto.
  function handleReady() {
    if (isHost || isReady) return;

    runAction(async () => {
      const updatedRoom = await putReady(
        roomCode,
        playerId
      );

      if (updatedRoom?.players) {
        processRoom(updatedRoom);
      } else {
        const refreshedRoom = await getRoom(roomCode);
        processRoom(refreshedRoom);
      }
    });
  }

  // Host remove outro jogador.
  function handleKick(targetPlayerId) {
    if (!isHost || targetPlayerId === playerId) {
      return;
    }

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

  // Jogador sai voluntariamente da sala.
  function handleLeave() {
    runAction(async () => {
      await exitRoom(roomCode, playerId);
      callbacksRef.current.onLeave();
    });
  }

  // Host inicia a partida.
  function handleStart() {
    if (!isHost || !allReady) return;

    runAction(async () => {
      const match = await startRoom(
        roomCode,
        playerId
      );

      if (!match?.match_id) {
        throw new Error(
          "O servidor não retornou o ID da partida."
        );
      }

      callbacksRef.current.onStart(match.match_id);
    });
  }

  return (
    <main className="lobby-wrap htbg">
      <h1
        className="logo"
        style={{ fontSize: "2.5rem" }}
      >
        POL<em>IS</em>
      </h1>

      <section className="card-dark lobby-card anim-up">
        <span className="lbl lbl-light">
          SALA DE ESPERA
        </span>

        <h2 style={{ margin: "10px 0" }}>
          Código: {roomCode}
        </h2>

        <p
          style={{
            color: "var(--tx-d)",
            marginBottom: 16,
          }}
        >
          Jogadores: {playerEntries.length}/{MAX_PLAYERS}
        </p>

        <div
          className="prog-wrap"
          style={{ marginBottom: 18 }}
        >
          <div
            className="prog-fill"
            style={{
              width: `${
                (playerEntries.length / MAX_PLAYERS) * 100
              }%`,
            }}
          />
        </div>

        <div className="players-grid">
          {playerEntries.map(([id, roomPlayer]) => (
            <div className="p-slot" key={id}>
              <div
                className={`p-av ${
                  roomPlayer.host ? "host" : ""
                }`}
              >
                {roomPlayer.host ? "👑" : "👤"}
              </div>

              <div
                style={{
                  flex: 1,
                  minWidth: 0,
                }}
              >
                <strong
                  style={{
                    display: "block",
                    overflowWrap: "anywhere",
                  }}
                >
                  {playerNames[id] ?? id}

                  {id === playerId ? " (você)" : ""}
                </strong>

                <span
                  className={`badge ${
                    roomPlayer.host
                      ? "bg-gold"
                      : roomPlayer.ready
                        ? "bg-green"
                        : "bg-gray"
                  }`}
                  style={{ marginTop: 5 }}
                >
                  {roomPlayer.host
                    ? "HOST"
                    : roomPlayer.ready
                      ? "PRONTO"
                      : "AGUARDANDO"}
                </span>
              </div>

              {isHost && id !== playerId && (
                <button
                  type="button"
                  className="btn btn-danger"
                  onClick={() => handleKick(id)}
                  disabled={loading}
                  title="Remover jogador"
                  aria-label={`Remover ${
                    playerNames[id] ?? id
                  }`}
                >
                  ✕
                </button>
              )}
            </div>
          ))}

          {Array.from({
            length: emptySlots,
          }).map((_, index) => (
            <div
              className="p-slot empty"
              key={`empty-${index}`}
            >
              <div className="p-av">+</div>

              <span>
                Aguardando jogador...
              </span>
            </div>
          ))}
        </div>

        <hr className="sep" />

        <p
          style={{
            color: "var(--tx-d)",
            textAlign: "center",
            marginBottom: 14,
          }}
        >
          {isHost
            ? allReady
              ? "Todos estão prontos! A partida pode começar."
              : "Aguarde quatro jogadores e todos ficarem prontos."
            : isReady
              ? "Você está pronto. Aguarde o host iniciar."
              : "Marque pronto para participar da partida."}
        </p>

        {error && (
          <p
            role="alert"
            style={{
              color: "var(--red)",
              textAlign: "center",
              marginBottom: 12,
            }}
          >
            {error}
          </p>
        )}

        <div className="btn-row">
          {isHost ? (
            <button
              type="button"
              className="btn btn-gold"
              onClick={handleStart}
              disabled={loading || !allReady}
            >
              {loading
                ? "AGUARDE..."
                : "INICIAR PARTIDA"}
            </button>
          ) : (
            <button
              type="button"
              className="btn btn-gold"
              onClick={handleReady}
              disabled={loading || isReady}
            >
              {isReady
                ? "✓ PRONTO"
                : "ESTOU PRONTO"}
            </button>
          )}

          <button
            type="button"
            className="btn btn-danger"
            onClick={handleLeave}
            disabled={loading}
          >
            SAIR DA SALA
          </button>
        </div>
      </section>
    </main>
  );
}