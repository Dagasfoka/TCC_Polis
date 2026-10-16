import { useState } from "react";
import {
  createPrivateRoom,
  joinRandomRoom,
  joinRoom,
  chooseAvatar,
} from "../service/api.jsx";
import { getAvatarImage } from "../utils/avatarAssets.js";

export default function Menu({ player, onEnterRoom, onLogout }) {

  const avatars = [
    "avatar_1",
    "avatar_2",
    "avatar_3",
    "avatar_4",
  ];

  const [roomCode, setRoomCode] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [showAvatarModal, setShowAvatarModal] = useState(false);
  const [selectedAvatar, setSelectedAvatar] = useState(player?.avatar_id || null);

  async function handleChooseAvatar(avatarId) {
    try {
      setLoading(true);
      setError("");

      const updatedPlayer = await chooseAvatar(
        player.player_id,
        avatarId
      );

      console.log("PLAYER ATUALIZADO:", updatedPlayer);


      setSelectedAvatar(updatedPlayer.avatar_id);
      setShowAvatarModal(false);

    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  }
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
          bottom: -34px;
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
          display: inline-block;
          padding: 2px 12px 4px;
          background: #000000;
          color: #ffffff;
          font-family: "Coolvetica", sans-serif;
          font-weight: 800;
          font-size: 28px;
          letter-spacing: calc(0.04em + 1px);
          white-space: nowrap;
          -webkit-text-stroke: 5.5px #000;
          paint-order: stroke fill;
          text-shadow:
            4px 4px 0 #000,
            5px 4px 0 #000,
            4px 5px 0 #000,
            5px 5px 0 #000;
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
          display: flex;
          flex-direction: column;
          align-items: center;
        }

        .code-btn-submit {
          position: relative;
          z-index: 2;
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
          position: relative;
          z-index: 1;
          transform: none;
          margin-top: -19px;
          width: 270px;
          height: 64px;
          background: url("/DIGITARCODIGO.png") center / 100% 100% no-repeat;
          border: none;
          outline: none;
          color: #ffffff;
          font-family: 'Fira Code', monospace;
          font-weight: 800;
          font-size: 22px;
          text-align: center;
          letter-spacing: 4px;
          text-transform: uppercase;
        }

        .code-input-overlay::placeholder {
          color: rgba(255, 255, 255, 0.5);
        }

        .status-msg {
          position: absolute;
          right: 10px;
          bottom: 16px;
          margin: 0;
          font-size: 14px;
          font-weight: 700;
          text-align: right;
          width: 340px;
        }

        /* ==============================
   MODAL DE ESCOLHA DE AVATAR
   ============================== */

.avatar-modal-overlay {
  position: fixed;
  inset: 0;

  background: rgba(5, 10, 20, 0.78);

  display: flex;
  align-items: center;
  justify-content: center;

  z-index: 9999;

  backdrop-filter: blur(4px);
}

.avatar-modal-box {
  position: relative;

  width: 760px;
  max-width: 92%;

  min-height: 420px;

  background:
    linear-gradient(
      180deg,
      rgba(30, 46, 78, 0.98),
      rgba(13, 18, 29, 0.98)
    );

  border: 2px solid #2e3e6e;
  border-radius: 16px;

  box-shadow:
    0 20px 60px rgba(0, 0, 0, 0.75),
    inset 0 0 25px rgba(76, 110, 245, 0.08);

  padding: 35px 40px 40px;

  font-family: 'Fira Code', monospace;
  color: #ffffff;

  text-align: center;
}

.avatar-modal-title {
  font-size: 25px;
  font-weight: 800;

  margin-bottom: 30px;

  color: #ffffff;

  text-shadow: 0 3px 8px rgba(0, 0, 0, 0.7);
}

.avatar-modal-close {
  position: absolute;

  top: 15px;
  right: 18px;

  width: 38px;
  height: 38px;

  border: none;
  border-radius: 8px;

  background: rgba(255, 255, 255, 0.08);

  color: #ffffff;

  font-family: 'Fira Code', monospace;
  font-size: 22px;
  font-weight: 800;

  cursor: pointer;

  transition:
    transform 0.15s ease,
    background 0.15s ease;
}

.avatar-modal-close:hover {
  transform: scale(1.08);
  background: rgba(255, 82, 82, 0.7);
}

.avatar-options {
  display: grid;

  grid-template-columns: repeat(4, 1fr);

  gap: 22px;

  align-items: center;
  justify-items: center;
}

.avatar-option {
  width: 140px;
  height: 170px;

  border: 2px solid #2e3e6e;
  border-radius: 14px;

  background: rgba(13, 18, 29, 0.75);

  display: flex;
  align-items: center;
  justify-content: center;

  cursor: pointer;

  padding: 10px;

  transition:
    transform 0.15s ease,
    border-color 0.15s ease,
    box-shadow 0.15s ease,
    background 0.15s ease;
}

.avatar-option:hover:not(:disabled) {
  transform: translateY(-5px) scale(1.04);

  border-color: #4c6ef5;

  background: rgba(27, 38, 71, 0.95);

  box-shadow:
    0 10px 25px rgba(0, 0, 0, 0.5),
    0 0 15px rgba(76, 110, 245, 0.35);
}

.avatar-option:disabled {
  opacity: 0.55;
  cursor: not-allowed;
}

.avatar-option.selected {
  border-color: #6d8cff;

  background: rgba(59, 91, 219, 0.25);

  box-shadow:
    0 0 0 3px rgba(76, 110, 245, 0.2),
    0 10px 25px rgba(0, 0, 0, 0.5);
}

.avatar-option img {
  width: 115px;
  height: 145px;

  object-fit: contain;

  display: block;

  filter: drop-shadow(
    0px 7px 8px rgba(0, 0, 0, 0.45)
  );
}

.avatar-button {
  position: absolute;
  bottom: 160px;
  width: 260px;
  background: none;
  border: none;
  padding: 0;
  cursor: pointer;
  z-index: 2;
  transition: transform 0.15s ease;
}

.avatar-button:hover {
  transform: scale(1.04);
}

.avatar-button .avatar-sapo {
  position: static;
  width: 260px;
  display: block;
}

        .loading-msg { color: #ffca28; }
        .error-msg { color: #f04444; }
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

    <img
      src="/perfil.png"
      className="badge-perfil"
      alt="PERFIL"
    />

    <button
      type="button"
      className="avatar-button"
      onClick={() => setShowAvatarModal(true)}
      title="Trocar avatar"
    >
      <img
        src={getAvatarImage(selectedAvatar)}
        className="avatar-sapo"
        alt="Avatar do jogador"
      />
    </button>

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
      <img
        src="/aleatoria.png"
        alt="Sala Aleatória"
      />
    </button>


    {/* Criar Sala Privada */}
    <button
      onClick={handleCreatePrivateRoom}
      disabled={loading}
      className="btn-action-img"
    >
      <img
        src="/criar.png"
        alt="Criar Sala"
      />
    </button>


    {/* Entrar com Código */}
    <form
      onSubmit={handleJoinRoom}
      className="code-form-wrapper"
    >

      <button
        type="submit"
        disabled={loading}
        className="code-btn-submit"
        title="Entrar com Código"
      >
        <img
          src="/entrar.png"
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
          setRoomCode(
            event.target.value.toUpperCase()
          )
        }
        disabled={loading}
        className="code-input-overlay"
      />

    </form>


    {loading && (
      <p className="status-msg loading-msg">
        Carregando...
      </p>
    )}

    {error && (
      <p
        className="status-msg error-msg"
        role="alert"
      >
        {error}
      </p>
    )}

  </div>

</div>


{/* ==============================
    MODAL DE AVATAR
================================ */}

{showAvatarModal && (
  <div className="avatar-modal-overlay">

    <div className="avatar-modal-box">

      <button
        type="button"
        className="avatar-modal-close"
        onClick={() =>
          setShowAvatarModal(false)
        }
      >
        ×
      </button>

      <h2 className="avatar-modal-title">
        ESCOLHA SEU AVATAR
      </h2>

      <div className="avatar-options">

        {avatars.map((avatar) => (
          <button
            key={avatar}
            type="button"
            className={`avatar-option ${
              selectedAvatar === avatar
                ? "selected"
                : ""
            }`}
            disabled={loading}
            onClick={() =>
              handleChooseAvatar(avatar)
            }
          >
            <img
              src={getAvatarImage(avatar)}
              alt={avatar}
            />
          </button>
        ))}

      </div>

    </div>

  </div>
)}

</div>
  
);

}
