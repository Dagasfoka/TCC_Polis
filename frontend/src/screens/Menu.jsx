import { useState } from "react";

import {
  createPublicRoom,
  createPrivateRoom,
  joinRandomRoom,
  joinRoom,
} from "../service/api.jsx";

export default function Menu({ player, onEnterRoom, onLogout, }) {
  const [roomCode, setRoomCode] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  // Criar sala privada
  async function handleCreatePrivateRoom() {
    try {
      setLoading(true);
      setError("");

      const room = await createPrivateRoom(
        player.player_id
      );

      onEnterRoom(room);
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleCreatePublicRoom() {
    try {
      setLoading(true);
      setError("");

      const room = await createPublicRoom(
        player.player_id
      );

      onEnterRoom(room);
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  }

  // Procurar sala pública aleatória
  async function handleRandomRoom() {
    try {
      setLoading(true);
      setError("");

      const room = await joinRandomRoom(
        player.player_id
      );

      onEnterRoom(room);
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  }

  // Entrar usando código
  async function handleJoinRoom() {
    const code = roomCode.trim();

    if (!code) {
      setError("Digite o código da sala.");
      return;
    }

    try {
      setLoading(true);
      setError("");

      const room = await joinRoom(
        code,
        player.player_id
      );

      onEnterRoom(room);
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="menu-container">
      <h1>POLIS</h1>

      <h2>Bem-vindo, {player.username}!</h2>

      <button
        onClick={onLogout}
        disabled={loading}
      >
        SAIR
      </button>

      <button
        onClick={handleCreatePublicRoom}
        disabled={loading}
      >
        CRIAR SALA PÚBLICA
      </button>

      <button
        onClick={handleCreatePrivateRoom}
        disabled={loading}
      >
        CRIAR SALA PRIVADA
      </button>

      <button
        onClick={handleRandomRoom}
        disabled={loading}
      >
        PARTIDA ALEATÓRIA
      </button>
      <div className="join-room">
        <input
          type="text"
          placeholder="Código da sala"
          value={roomCode}
          onChange={(event) =>
            setRoomCode(event.target.value.toUpperCase())
          }
          disabled={loading}
        />

        <button
          onClick={handleJoinRoom}
          disabled={loading}
        >
          ENTRAR COM CÓDIGO
        </button>
      </div>

      {loading && <p>Carregando...</p>}

      {error && (
        <p role="alert">
          {error}
        </p>
      )}
    </div>
  );
}