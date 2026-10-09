import { useState } from "react";
import {
  createPrivateRoom,
  joinRandomRoom,
  joinRoom,
} from "../service/api.jsx";

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
          cursor: pointer;
          padding: 0;
        }

        .top-login-link-btn img {
          height: 28px;
          width: auto;
          display: block;
          transition: transform 0.15s ease;
        }

        .top-login-link-btn:hover img {
          transform: scale(1.05);
        }

        .main-card {
          width: 100%;
          max-width: 1020px;
          height: 560px;
          position: relative;
          border-radius: 16px;
          overflow: hidden;
          box-shadow: 0 20px 50px rgba(0, 0, 0, 0.7);
          background: #1b2647 url('/fundomenu.png') no-repeat center center / cover;
          display: flex;
        }

        .profile-section {
          width: 48%;
          height: 100%;
          position: relative;
          z-index: 2;
          display: flex;
          justify-content: center;
          align-items: center;
        }

        .retangulo-bg {
          position: absolute;
          width: 330px;
          height: 380px;
          top: 85px;
          z-index: 1;
          object-fit: contain;
        }

        .badge-perfil {
          position: absolute;
          top: 45px;
          width: 300px;
          z-index: 4;
        }

        .avatar-sapo {
          position: absolute;
          bottom: 160px;
          width: 260px;
          z-index: 2;
        }

        .podium-wrapper {
          position: absolute;
          bottom: -10px;
          width: 290px;
          z-index: 3;
        }

        .podium-wrapper img {
          width: 100%;
          display: block;
        }

        .player-name {
          position: absolute;
          top: 14px;
          left: 50%;
          transform: translateX(-50%);
          color: #ffffff;
          font-weight: 800;
          font-size: 20px;
          white-space: nowrap;
          text-shadow: 0 2px 4px rgba(0,0,0,0.7);
        }

        .actions-section {
          width: 52%;
          height: 100%;
          position: relative;
          z-index: 2;
          display: flex;
          flex-direction: column;
          align-items: flex-end;
          justify-content: center;
          padding-right: 40px;
          gap: 18px;
        }

        .btn-action-img {
          background: none;
          border: none;
          cursor: pointer;
          transition: transform 0.15s ease;
          display: block;
          padding: 0;
        }

        .btn-action-img:hover:not(:disabled) {
          transform: scale(1.03);
        }

        .btn-action-img:disabled {
          opacity: 0.6;
          cursor: not-allowed;
        }

        .btn-action-img img {
          width: 340px;
          height: auto;
          display: block;
          filter: drop-shadow(0px 6px 12px rgba(0, 0, 0, 0.3));
        }

        /* CONTAINER ÚNICO COM APENAS A IMAGEM ORIGINAL */
        .code-form-wrapper {
          position: relative;
          width: 340px;
        }

        .code-btn-submit {
          background: none;
          border: none;
          padding: 0;
          cursor: pointer;
          display: block;
          width: 100%;
          transition: transform 0.15s ease;
        }

        .code-btn-submit:hover:not(:disabled) {
          transform: scale(1.03);
        }

        .code-bg-img {
          width: 340px;
          height: auto;
          display: block;
          filter: drop-shadow(0px 6px 12px rgba(0, 0, 0, 0.3));
        }

        /* CAIXA DE INPUT TRANSPARENTE ALINHADA PERFEITAMENTE SOBRE O ESPAÇO MARROM */
        .code-input-overlay {
          position: absolute;
          bottom: 12px;
          left: 50%;
          transform: translateX(-50%);
          width: 270px;
          height: 48px;
          background: transparent;
          border: none;
          outline: none;
          color: #ffffff;
          font-family: 'Fira Code', monospace;
          font-weight: 800;
          font-size: 22px;
          text-align: center;
          letter-spacing: 4px;
          text-transform: uppercase;
          z-index: 3;
        }

        .code-input-overlay::placeholder {
          color: rgba(255, 255, 255, 0.5);
        }

        .status-msg {
          font-size: 14px;
          font-weight: 700;
          text-align: right;
          width: 340px;
        }

        .loading-msg { color: #ffca28; }
        .error-msg { color: #ff5252; }
      `}</style>

      {/* Topo */}
      <div className="header-bar-lobby">
        <div className="header-logo">
          <img src="/polis.png" alt="Logo Polis" />
        </div>
        <button
          onClick={onLogout}
          disabled={loading}
          className="top-login-link-btn"
          title="Sair"
        >
          <img src="/sair.png" alt="Sair" />
        </button>
      </div>

      {/* Card Principal */}
      <div className="main-card">
        {/* Esquerda: Perfil */}
        <div className="profile-section">
          <img
            src="/retangulo.png"
            className="retangulo-bg"
            alt="Fundo Retângulo Azul"
          />
          <img src="/perfil.png" className="badge-perfil" alt="PERFIL" />

          <img
            src="/sapoestendido.png"
            className="avatar-sapo"
            alt="Avatar Sapo"
          />

          <div className="podium-wrapper">
            <img src="/podio.png" alt="Pódio" />
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
            <img src="/aleatoria.png" alt="Sala Aleatória" />
          </button>

          {/* Criar Sala Privada */}
          <button
            onClick={handleCreatePrivateRoom}
            disabled={loading}
            className="btn-action-img"
          >
            <img src="/criar.png" alt="Criar Sala" />
          </button>

          {/* Entrar com Código sem duplicação de elementos */}
          <form onSubmit={handleJoinRoom} className="code-form-wrapper">
            <button
              type="submit"
              disabled={loading}
              className="code-btn-submit"
              title="Entrar com Código"
            >
              <img
                src="/codigo.png"
                alt="Entrar com Código"
                className="code-bg-img"
              />
            </button>
            <input
              type="text"
              maxLength={7}
              placeholder="CÓDIGO"
              value={roomCode}
              onChange={(event) =>
                setRoomCode(event.target.value.toUpperCase())
              }
              disabled={loading}
              className="code-input-overlay"
            />
          </form>

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