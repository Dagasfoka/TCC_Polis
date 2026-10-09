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
    event.preventDefault();

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
    event.preventDefault();

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
    event.preventDefault();

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

      <h1>POLIS</h1>


      {/* =========================
          GUEST
      ========================== */}

      {mode === "guest" && (
        <>

          <h2>Jogar como convidado</h2>

          <form onSubmit={handleGuest}>

            <input
              type="text"
              placeholder="Seu nickname"
              value={nickname}
              maxLength={30}
              disabled={loading}
              onChange={(event) =>
                setNickname(event.target.value)
              }
            />

            <button
              type="submit"
              disabled={loading}
            >
              {loading
                ? "Entrando..."
                : "JOGAR COMO GUEST"}
            </button>

          </form>


          <p>OU</p>


          <button
            type="button"
            disabled={loading}
            onClick={() =>
              changeMode("login")
            }
          >
            ENTRAR NA CONTA
          </button>


          <button
            type="button"
            disabled={loading}
            onClick={() =>
              changeMode("register")
            }
          >
            CRIAR UMA CONTA
          </button>

        </>
      )}


      {/* =========================
          LOGIN
      ========================== */}

      {mode === "login" && (
        <>

          <h2>Entrar na conta</h2>

          <form
            onSubmit={handleAccountLogin}
          >

            <input
              type="text"
              placeholder="Username"
              value={username}
              maxLength={30}
              disabled={loading}
              onChange={(event) =>
                setUsername(
                  event.target.value
                )
              }
            />


            <input
              type="password"
              placeholder="Senha"
              value={password}
              disabled={loading}
              onChange={(event) =>
                setPassword(
                  event.target.value
                )
              }
            />


            <button
              type="submit"
              disabled={loading}
            >
              {loading
                ? "Entrando..."
                : "ENTRAR"}
            </button>

          </form>


          <button
            type="button"
            disabled={loading}
            onClick={() =>
              changeMode("register")
            }
          >
            NÃO TENHO CONTA
          </button>


          <button
            type="button"
            disabled={loading}
            onClick={() =>
              changeMode("guest")
            }
          >
            VOLTAR
          </button>

        </>
      )}


      {/* =========================
          CADASTRO
      ========================== */}

      {mode === "register" && (
        <>

          <h2>Criar conta</h2>

          <form
            onSubmit={handleRegister}
          >

            <input
              type="text"
              placeholder="Username"
              value={username}
              maxLength={30}
              disabled={loading}
              onChange={(event) =>
                setUsername(
                  event.target.value
                )
              }
            />


            <input
              type="password"
              placeholder="Senha"
              value={password}
              disabled={loading}
              onChange={(event) =>
                setPassword(
                  event.target.value
                )
              }
            />


            <button
              type="submit"
              disabled={loading}
            >
              {loading
                ? "Criando conta..."
                : "CADASTRAR"}
            </button>

          </form>


          <button
            type="button"
            disabled={loading}
            onClick={() =>
              changeMode("login")
            }
          >
            JÁ TENHO CONTA
          </button>


          <button
            type="button"
            disabled={loading}
            onClick={() =>
              changeMode("guest")
            }
          >
            VOLTAR
          </button>

        </>
      )}


      {error && (
        <p role="alert">
          {error}
        </p>
      )}

    </div>
  );
}