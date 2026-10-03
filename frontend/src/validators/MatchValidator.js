export class MatchValidator {
  MatchIDExists(matchId) {
    return Boolean(matchId);
  }
    MatchExists(savedMatch) {
        if (!savedMatch?.match_id) {
            throw new Error("Partida não encontrada");
    }
  }
}