import { useState } from "react";

import {
  createPlayer,
  createUser,
  loginUser,
} from "../service/api.jsx";

export default function Login({ onLogin }) {

  // guest | login | register
  const [mode, setMode] = useState("guest");

  const [nickname, setNickname] = useState("");

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");


  // ==============================
  // GUEST
  // ==============================

  async function handleGuest(event) {
    if (event) event.preventDefault();

    const name = nickname.trim();

    if (!name) {
      setError("Digite um nickname.");
      return;
    }

    try {
      setLoading(true);
      setError("");

      const player = await createPlayer(name);

      localStorage.setItem(
        "player_id",
        player.player_id
      );

      // Guest não possui User.
      localStorage.removeItem("user_id");

      onLogin(player);

    } catch (error) {

      setError(error.message);

    } finally {

      setLoading(false);
    }
  }


  // ==============================
  // LOGIN DE USUÁRIO
  // ==============================

  async function handleAccountLogin(event) {
    if (event) event.preventDefault();

    const name = username.trim();

    if (!name || !password) {
      setError(
        "Preencha username e senha."
      );
      return;
    }

    try {
      setLoading(true);
      setError("");

      // Busca o User no SQL.
      const user = await loginUser(
        name,
        password
      );

      // Cria o Player temporário no Redis
      // usando o username da conta.
      const player = await createPlayer(
        user.username
      );

      localStorage.setItem(
        "user_id",
        user.user_id
      );

      localStorage.setItem(
        "player_id",
        player.player_id
      );

      onLogin(player);

    } catch (error) {

      setError(error.message);

    } finally {

      setLoading(false);
    }
  }


  // ==============================
  // CADASTRO
  // ==============================

  async function handleRegister(event) {
    if (event) event.preventDefault();

    const name = username.trim();

    if (!name || !password) {
      setError(
        "Preencha username e senha."
      );
      return;
    }

    try {
      setLoading(true);
      setError("");

      // Cria User no SQL.
      const user = await createUser(
        name,
        password
      );

      // Cria Player temporário no Redis.
      const player = await createPlayer(
        user.username
      );

      localStorage.setItem(
        "user_id",
        user.user_id
      );

      localStorage.setItem(
        "player_id",
        player.player_id
      );

      onLogin(player);

    } catch (error) {

      setError(error.message);

    } finally {

      setLoading(false);
    }
  }


  // ==============================
  // TROCAR MODO
  // ==============================

  function changeMode(newMode) {
    setMode(newMode);
    setError("");
    setPassword("");
  }


  return (
    <div className="login-container">

      {/* CSS embutido das 3 telas bonitas */}
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;600;700;800&display=swap');

        .login-container {
          font-family: 'Fira Code', monospace;
          background-color: #0d121d;
          background-image: url('images/fundo.png');
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
          box-sizing: border-box;
          color: #ffffff;
        }

        .header-bar, .header-logo {
          width: 100%;
          max-width: 1020px;
          display: flex;
          align-items: center;
          justify-content: center;
          margin-bottom: 15px;
        }

        .header-logo img {
          height: 55px;
          width: auto;
          display: block;
        }

        /* HTML INÍCIO (GUEST) */
        .main-card-inicio {
          width: 100%;
          max-width: 1020px;
          height: 560px;
          position: relative;
          border-radius: 16px;
          overflow: hidden;
          box-shadow: 0 20px 50px rgba(0, 0, 0, 0.7);
          background-color: #1e2638;
          background-image: url('images/fundoinicio.png');
          background-size: cover;
          background-position: center;
          margin-top: -10px;
        }

        .btn-login-container,
        .btn-cadastro-container {
          background: none;
          border: none;
          position: absolute;
          top: 38%;
          cursor: pointer;
          display: block;
          padding: 0;
          transition: transform 0.15s ease;
        }

        .btn-login-container { left: 8%; }
        .btn-cadastro-container { right: 8%; }

        .btn-login-container img,
        .btn-cadastro-container img {
          width: 250px;
          height: auto;
          display: block;
          filter: drop-shadow(0px 8px 16px rgba(0, 0, 0, 0.4));
        }

        .btn-login-container:hover,
        .btn-cadastro-container:hover {
          transform: scale(1.05);
        }

        .btn-anonimo-container {
          position: absolute;
          left: 50%;
          top: 18%;
          transform: translateX(-50%);
          width: 280px;
          transition: transform 0.15s ease;
        }

        .btn-anonimo-container:hover {
          transform: translateX(-50%) scale(1.03);
        }

        .btn-anonimo-img {
          width: 100%;
          height: auto;
          display: block;
          filter: drop-shadow(0px 8px 16px rgba(0, 0, 0, 0.4));
          cursor: pointer;
        }

        .input-nome-anonimo {
          position: absolute;
          bottom: 8px;
          left: 50%;
          transform: translateX(-50%);
          width: 80%;
          height: 65px;
          background: transparent;
          border: none;
          outline: none;
          font-family: 'Fira Code', monospace;
          font-weight: 700;
          font-size: 1rem;
          color: #333333;
          text-align: center;
        }

        .input-nome-anonimo::placeholder {
          color: #555555;
          font-weight: 600;
          opacity: 0.9;
        }

        /* HTML LOGIN E CADASTRO */
        .main-card {
          width: 100%;
          max-width: 1020px;
          height: 560px;
          position: relative;
          border-radius: 16px;
          overflow: hidden;
          box-shadow: 0 20px 50px rgba(0, 0, 0, 0.7);
          background-color: #1b2647;
          display: flex;
          align-items: center;
          justify-content: flex-end;
          padding: 40px;
        }

        .card-bg-image {
          position: absolute;
          left: 0;
          top: 0;
          height: 100%;
          width: auto;
          object-fit: cover;
        }

        .form-box {
          position: relative;
          width: 380px;
          background: rgba(13, 18, 29, 0.85);
          border: 2px solid #2e3e6e;
          border-radius: 12px;
          padding: 35px 25px 20px 25px;
          z-index: 2;
          box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        }

        .form-title-banner {
          position: absolute;
          top: -25px;
          left: 50%;
          transform: translateX(-50%);
        }

        .form-title-banner img {
          height: 45px;
          width: auto;
        }

        .input-group {
          margin-bottom: 14px;
          display: flex;
          flex-direction: column;
        }

        .input-group label {
          color: #a0aec0;
          font-size: 0.85rem;
          margin-bottom: 4px;
          font-weight: 600;
        }

        .input-group input {
          width: 100%;
          padding: 10px 12px;
          border-radius: 6px;
          border: 1px solid #2e3e6e;
          background: #0d121d;
          color: #ffffff;
          font-family: 'Fira Code', monospace;
          font-size: 0.95rem;
          outline: none;
        }

        .input-group input:focus {
          border-color: #4c6ef5;
        }

        .btn-submit-action {
          width: 100%;
          padding: 12px;
          margin-top: 10px;
          background: #3b5bdb;
          color: #ffffff;
          border: none;
          border-radius: 6px;
          font-family: 'Fira Code', monospace;
          font-weight: 700;
          font-size: 1rem;
          cursor: pointer;
          transition: background 0.2s ease;
        }

        .btn-submit-action:hover:not(:disabled) {
          background: #4c6ef5;
        }

        .btn-submit-action:disabled {
          opacity: 0.6;
          cursor: not-allowed;
        }

        .login-links, .form-links {
          display: flex;
          justify-content: space-between;
          margin-top: 15px;
        }

        .link-btn {
          background: none;
          border: none;
          color: #7986ac;
          font-family: 'Fira Code', monospace;
          font-size: 0.8rem;
          cursor: pointer;
          text-decoration: underline;
        }

        .link-btn:hover {
          color: #ffffff;
        }

        .hidden-submit {
          display: none;
        }

        .error-msg {
          color: #ff5252;
          font-size: 14px;
          font-weight: 700;
          text-align: center;
          margin-top: 10px;
        }
      `}</style>

      {/* Header com Logo comum a todas as telas */}
      <div className="header-bar">
        <div className="header-logo">
          <img src="images/polis.png" alt="Logo Polis" />
        </div>
      </div>


      {/* =========================
          GUEST (HTML INÍCIO)
      ========================== */}

      {mode === "guest" && (
        <div className="main-card-inicio">

          {/* Botão para mudar para tela de Login */}
          <button
            type="button"
            className="btn-login-container"
            disabled={loading}
            onClick={() => changeMode("login")}
          >
            <img src="images/botaologin.png" alt="Entrar em Conta" />
          </button>

          {/* Container Anônimo + Input */}
          <form onSubmit={handleGuest} className="btn-anonimo-container">
            <img
              src="images/botaoanon.png"
              alt="Entrar Anônimo"
              className="btn-anonimo-img"
              onClick={handleGuest}
            />
            <input
              type="text"
              id="anonName"
              className="input-nome-anonimo"
              placeholder="Digite seu nome"
              value={nickname}
              maxLength={30}
              disabled={loading}
              onChange={(event) => setNickname(event.target.value)}
            />
            <button type="submit" className="hidden-submit" disabled={loading} />
          </form>

          {/* Botão para mudar para tela de Cadastro */}
          <button
            type="button"
            className="btn-cadastro-container"
            disabled={loading}
            onClick={() => changeMode("register")}
          >
            <img src="images/botaocadastro.png" alt="Criar uma Conta" />
          </button>

        </div>
      )}


      {/* =========================
          LOGIN (HTML LOGIN)
      ========================== */}

      {mode === "login" && (
        <div className="main-card login-card">
          <img src="images/cachorro.png" alt="Ilustração Polis Login" className="card-bg-image" />

          <div className="form-box login-form-box">
            <div className="form-title-banner">
              <img src="images/login.png" alt="Login" />
            </div>

            <form onSubmit={handleAccountLogin}>

              <div className="input-group">
                <label htmlFor="username">Username</label>
                <input
                  type="text"
                  id="username"
                  placeholder="Seu username"
                  value={username}
                  maxLength={30}
                  disabled={loading}
                  onChange={(event) =>
                    setUsername(event.target.value)
                  }
                />
              </div>

              <div className="input-group">
                <label htmlFor="senha">Senha</label>
                <input
                  type="password"
                  id="senha"
                  placeholder="••••••••"
                  value={password}
                  disabled={loading}
                  onChange={(event) =>
                    setPassword(event.target.value)
                  }
                />
              </div>

              <button
                type="submit"
                className="btn-submit-action"
                disabled={loading}
              >
                {loading ? "Entrando..." : "ENTRAR"}
              </button>

              <div className="login-links">
                <button
                  type="button"
                  className="link-btn"
                  disabled={loading}
                  onClick={() => changeMode("register")}
                >
                  Não tenho conta
                </button>

                <button
                  type="button"
                  className="link-btn"
                  disabled={loading}
                  onClick={() => changeMode("guest")}
                >
                  Voltar
                </button>
              </div>

            </form>
          </div>
        </div>
      )}


      {/* =========================
          CADASTRO (HTML CADASTRO)
      ========================== */}

      {mode === "register" && (
        <div className="main-card menu-card">
          <img src="images/sapo.png" alt="Ilustração Polis Cadastro" className="card-bg-image" />

          <div className="form-box">
            <div className="form-title-banner">
              <img src="images/cadastro.png" alt="Cadastro" />
            </div>

            <form onSubmit={handleRegister}>

              <div className="input-group">
                <label htmlFor="reg-username">Username</label>
                <input
                  type="text"
                  id="reg-username"
                  placeholder="Digite seu username"
                  value={username}
                  maxLength={30}
                  disabled={loading}
                  onChange={(event) =>
                    setUsername(event.target.value)
                  }
                />
              </div>

              <div className="input-group">
                <label htmlFor="reg-password">Senha</label>
                <input
                  type="password"
                  id="reg-password"
                  placeholder="••••••••"
                  value={password}
                  disabled={loading}
                  onChange={(event) =>
                    setPassword(event.target.value)
                  }
                />
              </div>

              <button
                type="submit"
                className="btn-submit-action"
                disabled={loading}
              >
                {loading ? "Criando conta..." : "CADASTRAR"}
              </button>

              <div className="form-links">
                <button
                  type="button"
                  className="link-btn"
                  disabled={loading}
                  onClick={() => changeMode("login")}
                >
                  Já tenho conta
                </button>

                <button
                  type="button"
                  className="link-btn"
                  disabled={loading}
                  onClick={() => changeMode("guest")}
                >
                  Voltar
                </button>
              </div>

            </form>
          </div>
        </div>
      )}


      {/* Exibição do Erro */}
      {error && (
        <p className="error-msg" role="alert">
          {error}
        </p>
      )}

    </div>
  );
}