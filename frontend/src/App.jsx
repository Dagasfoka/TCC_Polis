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
  getPlayer,
} from "./service/api.jsx";

import { RoomValidator } from "./validators/RoomValidator.js";
import { PlayerValidator } from "./validators/PlayerValidator.js";


export default function App() {

  const roomValidator = new RoomValidator();
  const playerValidator = new PlayerValidator();

  const [screen, setScreen] = useState("login");

  const [player, setPlayer] = useState(null);
  const [room, setRoom] = useState(null);
  const [matchId, setMatchId] = useState(null);


  // ==============================
  // RECUPERAR PLAYER
  // ==============================

  useEffect(() => {

    async function restorePlayer() {

      const playerId =
        localStorage.getItem("player_id");

      if (
        !playerValidator.playerIdExists(playerId)
      ) {
        return;
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

          const currentRoom =
            await restoreRoom();

          if (
            roomValidator.roomExists(
              currentRoom
            ) &&
            roomValidator.playerInRoom(
              currentRoom,
              savedPlayer
            )
          ) {

            setRoom(currentRoom);
            setScreen("lobby");

          } else {

            clearRoomCode();
            setScreen("menu");
          }

        } catch (error) {

          console.error(
            "Não foi possível recuperar a sala:",
            error
          );

          clearRoomCode();
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


    restorePlayer();

  }, []);


  // ==============================
  // LOGIN / GUEST / CADASTRO
  // ==============================

  function handleLogin(playerData) {

    setPlayer(playerData);

    setScreen("menu");
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
          initialMatchId={matchId}
          initialPlayerId={
            player.player_id
          }
        />

      )}

    </>
  );
}