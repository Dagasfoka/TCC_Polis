const ROOM_CODE_KEY = "room_code";
import { getRoom } from "./api.jsx";

export function saveRoomCode(roomCode) {
  sessionStorage.setItem(ROOM_CODE_KEY, roomCode);
}

export function getSavedRoomCode() {
  return sessionStorage.getItem(ROOM_CODE_KEY);
}

export function clearRoomCode() {
  sessionStorage.removeItem(ROOM_CODE_KEY);
}

export async function restoreRoom() {
  const roomCode = getSavedRoomCode();

  if (!roomCode) return null;

  return await getRoom(roomCode);
}