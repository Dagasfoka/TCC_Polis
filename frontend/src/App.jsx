import { useState, useEffect, useLayoutEffect } from "react";

import DemoGameScreen from "./screens/DemoGameScreen.jsx";
import LoginScreen from "./screens/Login.jsx";
import MenuScreen from "./screens/Menu.jsx";
import LobbyScreen from "./screens/Lobby.jsx";
import TutorialBook from "./components/TutorialBook.jsx";

import {
  saveRoomCode,
  clearRoomCode,
  restoreRoom,
} from "./service/lobbySession.js";

import {
  saveMatchID,
  clearMatchID,
  getSavedMatchID,

} from "./service/matchSession.js"
import {
  getPlayer,
  deleteGuestPlayer,
  deleteUserPlayer,
} from "./service/api.jsx";

import { RoomValidator } from "./validators/RoomValidator.js";
import { PlayerValidator } from "./validators/PlayerValidator.js";
import { MatchValidator } from "./validators/MatchValidator.js";


export default function App() {
  const matchValidator = new MatchValidator()
  const roomValidator = new RoomValidator();
  const playerValidator = new PlayerValidator();

  const [screen, setScreen] = useState();

  const [player, setPlayer] = useState(null);
  const [room, setRoom] = useState(null);
  const [matchId, setMatchId] = useState(null);
  const [showTutorial, setShowTutorial] = useState(false);
  const [tutorialLeft, setTutorialLeft] = useState(null);
  const [tutorialTop, setTutorialTop] = useState(null);

  useLayoutEffect(() => {
    if (screen !== "menu" && screen !== "lobby") {
      setTutorialLeft(null);
      setTutorialTop(null);
      return undefined;
    }

    const alignWithCard = () => {
      const card = document.querySelector(".non-game-screen-zoom .main-card");
      const exitButton = document.querySelector(
        ".non-game-screen-zoom .top-login-link-btn, .non-game-screen-zoom .lobby-exit-btn"
      );
      if (card) {
        const cardBounds = card.getBoundingClientRect();
        setTutorialLeft(cardBounds.left);
        setTutorialTop(exitButton?.getBoundingClientRect().top ?? cardBounds.top);
      }
    };

    alignWithCard();
    window.addEventListener("resize", alignWithCard);
    return () => window.removeEventListener("resize", alignWithCard);
  }, [screen]);


  // ==============================
  // RECUPERAR PLAYER
  // ==============================

  useEffect(() => {

    async function restoreSession() {

      const playerId =
        localStorage.getItem("player_id");

      if (
        !playerValidator.playerIdExists(playerId)
      ) {
        setScreen("login");
        return
      }

      try {

        const savedPlayer =
          await getPlayer(playerId);

        playerValidator.playerExists(
          savedPlayer
        );

        setPlayer(savedPlayer);


        // ==========================
        // RECUPERAR SALA
        // ==========================
        try {
          const currentRoom = await restoreRoom();

          if (
            !roomValidator.roomExists(currentRoom) ||
            !roomValidator.playerInRoom(currentRoom, savedPlayer)
          ) {
            clearRoomCode();
            clearMatchID();
            setScreen("menu");
            return;
          }

          setRoom(currentRoom);

          const matchID = getSavedMatchID();

          if (matchValidator.MatchIDExists(matchID)) {
            setMatchId(matchID);
            setScreen("game");
          } else {
            clearMatchID();
            setScreen("lobby");
          }
        } catch (error) {

          console.error(
            "Não foi possível recuperar a sala:",
            error
          );

          clearRoomCode();
          clearMatchID()
          setScreen("menu");
        }


      } catch (error) {

        localStorage.removeItem(
          "player_id"
        );

        setPlayer(null);

        setScreen("login");
      }
    }


    restoreSession();

  }, []);


  // ==============================
  // LOGIN / GUEST / CADASTRO
  // ==============================
  // No App
  function handleMatchNotFound() {
    clearMatchID();
    setMatchId(null);
    setScreen("lobby");
  }
  function handleLogin(playerData) {

    setPlayer(playerData);

    setScreen("menu");
  }

  async function handleLogout() {
    const userId =
      localStorage.getItem("user_id");

    const playerId =
      localStorage.getItem("player_id");

    try {
      // Usuário cadastrado
      if (userId) {
        await deleteUserPlayer(
          Number(userId)
        );
      }

      // Guest
      else if (playerId) {
        await deleteGuestPlayer(
          playerId
        );
      }

    } catch (error) {
      console.error(
        "Erro ao apagar player no logout:",
        error
      );

    } finally {
      localStorage.removeItem(
        "user_id"
      );

      localStorage.removeItem(
        "player_id"
      );

      clearRoomCode();
      clearMatchID();

      setPlayer(null);
      setRoom(null);
      setMatchId(null);

      setScreen("login");
    }
  }
  // ==============================
  // ENTROU OU CRIOU SALA
  // ==============================

  function handleEnterRoom(roomData) {

    saveRoomCode(
      roomData.room_code
    );

    setMatchId(null);

    setRoom(roomData);

    setScreen("lobby");
  }


  // ==============================
  // SAIU DA SALA
  // ==============================

  function handleLeaveRoom() {

    clearRoomCode();

    setRoom(null);

    setMatchId(null);

    // Player continua existindo.
    // Volta para o menu.
    setScreen("menu");
  }


  // ==============================
  // INICIAR PARTIDA 
  // ==============================

  function handleStartGame(newMatchId) {

    setMatchId(newMatchId);

    setScreen("game");
    saveMatchID(newMatchId)
  }


  return (
    <>

      {screen === "login" && (
        <div className="non-game-screen-zoom">
          <LoginScreen
            onLogin={handleLogin}
          />
        </div>
      )}

 
      {screen === "menu" &&
        player && (
          <div className="non-game-screen-zoom">
            <MenuScreen
              player={player}
              onEnterRoom={handleEnterRoom}
              onLogout={handleLogout}
              onPlayerUpdate={setPlayer}
            />
          </div>
        )}



      {screen === "lobby" &&
        player &&
        room && (
          <div className="non-game-screen-zoom">
            <LobbyScreen
              player={player}
              room={room}
              onRoomUpdate={setRoom}
              onLeave={handleLeaveRoom}
              onStart={handleStartGame}
            />
          </div>
        )}


      {screen === "game" &&
        player &&
        matchId != null && (

          <DemoGameScreen
            onReturnRoom={() => setScreen("lobby")}
            onMatchNotFound={handleMatchNotFound}
            onLeaveRoom={handleLeaveRoom}
            initialMatchId={matchId}
            initialPlayerId={
              player.player_id
            }
          />

        )}

      {(screen === "menu" || screen === "lobby" || screen === "game") && (
        <button
          type="button"
          className={`polis-tutorial-open${screen === "game" ? " is-game" : " is-non-game"}`}
          onClick={() => setShowTutorial(true)}
          aria-label="Abrir tutorial de como jogar"
          aria-haspopup="dialog"
          style={screen !== "game" && tutorialLeft !== null
            ? { left: `${tutorialLeft}px`, top: `${tutorialTop}px` }
            : undefined}
        >
          <span>Como jogar?</span>
          {screen === "game" && (
            <img className="polis-tutorial-open-icon" src="/livro.png" alt="" aria-hidden="true" />
          )}
        </button>
      )}

      {showTutorial && <TutorialBook onClose={() => setShowTutorial(false)} />}

    </>
  );
}
