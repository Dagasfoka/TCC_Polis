export class RoomValidator {
  roomExists(room) {
    return Boolean(room);
  }

  playerInRoom(room, player) {
    return Boolean(room?.players?.[player?.player_id]);
  }
}