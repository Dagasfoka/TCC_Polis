import { useState } from "react";
import {
  createPublicRoom,
  createPrivateRoom,
  joinRandomRoom,
  joinRoom,
} from "../service/api.jsx";
import "./Menu.css"; // Estilos CSS trazidos do HTML bonito

export default function Menu({ player, onEnterRoom, onLogout }) {
  const [roomCode, setRoomCode] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  // Criar sala privada
  async function handleCreatePrivateRoom() {
    try {
      setLoading(true);
      setError("");

      const room = await createPrivateRoom(player.player_id);

      onEnterRoom(room);
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  }

  // Criar sala pública
  async function handleCreatePublicRoom() {
    try {
      setLoading(true);
      setError("");

      const room = await createPublicRoom(player.player_id);

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

      const room = await joinRandomRoom(player.player_id);

      onEnterRoom(room);
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  }

  // Entrar usando código
  async function handleJoinRoom(e) {
    if (e) e.preventDefault();
    const code = roomCode.trim();

    if (!code) {
      setError("Digite o código da sala.");
      return;
    }

    try {
      setLoading(true);
      setError("");

      const room = await joinRoom(code, player.player_id);

      onEnterRoom(room);
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="lobby-body">
      {/* Topo */}
      <div className="header-bar-lobby">
        <div className="header-logo">
          <img src="images/polis.png" alt="Logo Polis" />
        </div>
        <button
          onClick={onLogout}
          disabled={loading}
          className="top-login-link-btn"
          title="Sair"
        >
          <img src="images/sair.png" alt="Sair" />
        </button>
      </div>

      {/* Card Principal */}
      <div className="main-card">
        {/* Esquerda: Perfil */}
        <div className="profile-section">
          <img
            src="images/retangulo.png"
            className="retangulo-bg"
            alt="Fundo Retângulo Azul"
          />
          <img src="images/perfil.png" className="badge-perfil" alt="PERFIL" />

          <img
            src="images/sapoestendido.png"
            className="avatar-sapo"
            alt="Avatar Sapo"
          />

          <div className="podium-wrapper">
            <img src="images/podio.png" alt="Pódio" />
            <span className="player-name">
              {player?.username || player?.name || "Jogador"}
            </span>
          </div>
        </div>

        {/* Direita: Botões */}
        <div className="actions-section">
          {/* Sala Aleatória */}
          <button
            onClick={handleRandomRoom}
            disabled={loading}
            className="btn-action-img"
          >
            <img src="images/aleatoria.png" alt="Sala Aleatória" />
          </button>

          {/* Criar Sala Pública */}
          <button
            onClick={handleCreatePublicRoom}
            disabled={loading}
            className="btn-action-img"
          >
            <img src="images/criar.png" alt="Criar Sala Pública" />
          </button>

          {/* Criar Sala Privada */}
          <button
            onClick={handleCreatePrivateRoom}
            disabled={loading}
            className="btn-action-img"
          >
            <img src="images/criar.png" alt="Criar Sala Privada" />
          </button>

          {/* Form / Container de Entrar com Código */}
          <form onSubmit={handleJoinRoom} className="code-wrapper">
            <img
              src="images/codigo.png"
              alt="Entrar com Código"
              className="code-bg-img"
            />
            <input
              type="text"
              maxLength={7}
              placeholder="CÓDIGO"
              value={roomCode}
              onChange={(event) =>
                setRoomCode(event.target.value.toUpperCase())
              }
              disabled={loading}
              className="code-input"
            />
            <button type="submit" className="hidden-submit" disabled={loading}>
              Entrar
            </button>
          </form>

          {/* Mensagens de Feedback */}
          {loading && <p className="status-msg loading-msg">Carregando...</p>}
          {error && (
            <p className="status-msg error-msg" role="alert">
              {error}
            </p>
          )}
        </div>
      </div>
    </div>
  );
}