
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

import { getPlayer } from "./service/api.jsx";

export default function App() {

  const [screen, setScreen] = useState("login");

  const [player, setPlayer] = useState(null);

  const [room, setRoom] = useState(null);
  
  const [matchId, setMatchId] = useState(null);
  // Recuperar jogador salvo anteriormente
  useEffect(() => {
    
    async function restorePlayer() {
      const playerId = localStorage.getItem("player_id");

      if (!playerId) return;

      try {

        const savedPlayer = await getPlayer(playerId);

        if (!savedPlayer?.player_id) {
          throw new Error("Jogador não encontrado");
        }

        setPlayer(savedPlayer);

      try {
        const currentRoom = await restoreRoom();
        if (currentRoom && currentRoom.players?.[savedPlayer.player_id]) {
          setRoom(currentRoom);
          setScreen("lobby");
        } else {
          clearRoomCode();
          setScreen("menu");
        }
      } catch (error) {
        console.error("Não foi possível recuperar a sala:", error);
        setScreen("menu");
      }

      } catch (error) {

        localStorage.removeItem("player_id");

      }

    }

    restorePlayer();

  }, []);


  // Jogador criado
  function handleLogin(playerData) {

    setPlayer(playerData);

    setScreen("menu");

  }


  // Entrou ou criou uma sala
  function handleEnterRoom(roomData) {
  saveRoomCode(roomData.room_code)
  setMatchId(null);
  setRoom(roomData);
  setScreen("lobby");
}


//Saiu da sala 
function handleLeaveRoom() {
  clearRoomCode()
  setRoom(null);
  setMatchId(null);
  setScreen("menu");
}


  // Iniciar partida
  
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

      {screen === "menu" && player && (
        <MenuScreen
          player={player}
          onEnterRoom={handleEnterRoom}
        />
      )}

      {screen === "lobby" && player && room && (
        <LobbyScreen
          player={player}
          room={room}
          onRoomUpdate={setRoom}
          onLeave={handleLeaveRoom}
          onStart={handleStartGame}
        />
      )}

      {screen === "game" && player && matchId != null && (
        <DemoGameScreen
          initialMatchId={matchId}
          initialPlayerId={player.player_id}
        />
      )}

    </>
  );
}