export class PlayerValidator {
  playerIdExists(playerId) {
    return Boolean(playerId);
  }
    playerExists(savedPlayer) {
        if (!savedPlayer?.player_id) {
            throw new Error("Jogador não encontrado");
    }
  }
}