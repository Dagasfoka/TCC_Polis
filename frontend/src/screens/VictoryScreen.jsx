import { getAvatarImage } from "../utils/avatarAssets.js";
import { formatMission } from "../utils/missionUtils.js";

export default function VictoryScreen({
    victoryRanking,
    matchState,
    players,
    partyColors,
    onReturnRoom,
    onLeaveRoom,
}) {
    const victoryWinner = victoryRanking[0] ?? null;

    return (
        <div className="polis-victory-overlay" role="dialog" aria-modal="true" aria-label="Tela de vitória">
            <section className="polis-victory-screen">
                <img className="polis-victory-background" src="/fundovitoria.png" alt="" />
                <img className="polis-victory-title" src="/vencedor.png" alt="Vencedor" />

                <div className="polis-victory-winner-area">
                    <div className="polis-victory-winner-card">
                        <img
                            className="polis-victory-winner-avatar"
                            src={getAvatarImage(victoryWinner?.avatar_id)}
                            alt={victoryWinner ? `Avatar de ${victoryWinner.username}` : ""}
                            onError={(event) => {
                                event.currentTarget.src = getAvatarImage("avatar_3");
                            }}
                        />
                        <img className="polis-victory-winner-podium" src="/podio.png" alt="" />
                        <div className="polis-victory-winner-label">
                            <span className="polis-victory-winner-name">
                                {victoryWinner?.username ?? "Aguardando jogadores"}
                            </span>
                        </div>
                    </div>
                </div>

                <section className="polis-victory-missions" aria-label="Colocação e missões dos jogadores">
                    <img className="polis-victory-missions-art" src="/missoesrev.png" alt="Missões reveladas" />
                    <div className="polis-victory-missions-list">
                        {victoryRanking.map((rankedPlayer, index) => {
                            const storedMission = matchState?.missions?.find(
                                (item) => item.owner_id === rankedPlayer.player_id
                            );
                            const mission = (rankedPlayer.player_id === matchState?.your_player_id
                                ? matchState?.your_mission
                                : null) ?? rankedPlayer.mission ?? rankedPlayer.secret_mission ??
                                storedMission?.mission ?? storedMission;
                            const missionText = mission
                                ? formatMission(mission, players)
                                : "Missão não disponível.";

                            return (
                                <div
                                    className="polis-victory-player"
                                    key={rankedPlayer.player_id}
                                    style={{ "--victory-party-color": partyColors[rankedPlayer.party_id] ?? "#2b334e" }}
                                >
                                    <span className="polis-victory-rank">{index + 1}º</span>
                                    <div className="polis-victory-avatar-wrap">
                                        <img
                                            className="polis-victory-avatar"
                                            src={getAvatarImage(rankedPlayer.avatar_id)}
                                            alt={`Avatar de ${rankedPlayer.username}`}
                                            style={{ borderColor: partyColors[rankedPlayer.party_id] ?? "#2b334e" }}
                                            onError={(event) => {
                                                event.currentTarget.src = getAvatarImage("avatar_3");
                                            }}
                                        />
                                    </div>
                                    <div className="polis-victory-player-info">
                                        <div className="polis-victory-player-heading">
                                            <span className="polis-victory-player-name">{rankedPlayer.username}</span>
                                            <span className="polis-victory-player-count">
                                                {rankedPlayer.controlledTerritories} ⚑
                                            </span>
                                        </div>
                                        <span className="polis-victory-mission-text">{missionText}</span>
                                    </div>
                                </div>
                            );
                        })}
                        {victoryRanking.length === 0 && (
                            <p className="polis-victory-empty">Ainda não há jogadores na partida.</p>
                        )}
                    </div>
                </section>

                <button
                    type="button"
                    className="polis-victory-back"
                    onClick={() => onReturnRoom()}
                    aria-label="Voltar para a sala"
                >
                    <img src="/voltarsala.png" alt="Voltar para a sala" />
                </button>
                <button
                    type="button"
                    className="polis-victory-exit"
                    onClick={onLeaveRoom}
                    aria-label="Sair da partida"
                >
                    <img src="/sair2.png" alt="Sair" />
                </button>
            </section>
        </div>
    )
}