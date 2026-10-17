import { getAvatarImage } from "../utils/avatarAssets.js";
export default function PlayerCard({
    player,
    isCurrentTurn,
    isNext,
    isMe,
    partyColors,
    territories = [],
    side = "left",
}) {
    if (!player) {
        return null;
    }

    const partyColor = partyColors[player.party_id] ?? "#7f8c8d";

    const initials =
        player.username
            ?.trim()
            .split(/\s+/)
            .map((name) => name[0])
            .join("")
            .slice(0, 2)
            .toUpperCase() || "?";

    const controlledTerritories = territories.filter((territory) => territory.owner_id === player.player_id).length;
    const imageSuffix = side === "right" ? "d" : "e";

    return (
        <div
            className={[
                "polis-player-card",
                `polis-player-card-${side}`,
                isCurrentTurn ? "polis-player-current" : "",
                isMe ? "polis-player-me" : "",
            ]
                .filter(Boolean)
                .join(" ")}
            style={{ "--party-color": partyColor }}
        >
            <img
                className="polis-player-curtain"
                src="/Cortina.png"
                alt=""
                aria-hidden="true"
            />
            <div className="polis-player-polygon" aria-hidden="true" />
            {isNext && <div className="polis-next-label">Próximo</div>}


            <div className="polis-player-main">
                <div className="polis-player-avatar">
                    <img
                        src={getAvatarImage(player.avatar_id)}
                        alt={`Avatar de ${player.username}`}
                        onError={(event) => {
                            event.currentTarget.src = getAvatarImage("avatar_3");
                        }}
                    />
                </div>

                <div className="polis-player-stats">
                    <div className="polis-stat-row polis-stat-corruption" style={{ backgroundImage: `url(/corrupcao${imageSuffix}.png)` }}><span>{player.match_corruption ?? 0}%</span></div>
                    <div className="polis-stat-row polis-stat-money" style={{ backgroundImage: `url(/dinheiro${imageSuffix}.png)` }}><span>{player.match_money ?? 0}$</span></div>
                    <div className="polis-stat-row polis-stat-states" style={{ backgroundImage: `url(/estados${imageSuffix}.png)` }}><span>{controlledTerritories}</span></div>
                </div>
            </div>
            <div className="polis-player-name">{player.username}</div>
        </div>
    );
}