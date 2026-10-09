import { useState, useEffect } from "react";

import DemoGameScreen from "./screens/DemoGameScreen.jsx";
import LoginScreen from "./screens/Login.jsx";
import MenuScreen from "./screens/Menu.jsx";
import LobbyScreen from "./screens/Lobby.jsx";

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
        <LoginScreen
          onLogin={handleLogin}
        />
      )}


      {screen === "menu" &&
        player && (

          <MenuScreen
            player={player}
            onEnterRoom={handleEnterRoom}
            onLogout={handleLogout}
          />

        )}


      {screen === "lobby" &&
        player &&
        room && (

          <LobbyScreen
            player={player}
            room={room}
            onRoomUpdate={setRoom}
            onLeave={handleLeaveRoom}
            onStart={handleStartGame}
          />

        )}


      {screen === "game" &&
        player &&
        matchId != null && (

          <DemoGameScreen
            onMatchNotFound={handleMatchNotFound}
            initialMatchId={matchId}
            initialPlayerId={
              player.player_id
            }
          />

        )}

    </>
  );
}