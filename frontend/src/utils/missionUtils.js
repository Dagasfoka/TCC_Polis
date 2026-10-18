export function getPlayerNameById(playerId, players) {
    const player = players.find(
        (item) => item.player_id === playerId
    );

    if (!player) {
        return playerId ?? "jogador desconhecido";
    }

    const partyNames = {
        PR: "Vermelho",
        PD: "Amarelo",
        PA: "Azul",
        PV: "Verde",
    };

    const partyName = partyNames[player.party_id];

    return partyName
        ? `${player.username} (${partyName})`
        : player.username;
}

export function formatMission(mission, players = []) {
    if (!mission) {
        return "Missão não encontrada.";
    }

    const content = mission.content ?? {};

    if (mission.type === "state") {
        const states = content.state ?? [];

        if (states.length === 0) {
            return "Conquiste os territórios indicados pela sua missão.";
        }

        return `Conquiste os territórios: ${states.join(", ")}.`;
    }

    if (mission.type === "region") {
        const regions = content.region ?? [];

        if (regions.length === 0) {
            return "Conquiste os territórios indicados pela sua missão.";
        }

        return regions
            .map(
                (item) =>
                    `Conquiste ${item.quantity} território(s) em ${item.region}`
            )
            .join(" + ");
    }

    if (mission.type === "destruction") {
        const targetPlayerId = content.destruction;
        const alternativeStates = content.state ?? [];

        if (targetPlayerId) {
            const targetName = getPlayerNameById(targetPlayerId, players);

            if (alternativeStates.length > 0) {
                return `Destrua o jogador ${targetName}. Se essa missão for convertida, conquiste: ${alternativeStates.join(
                    ", "
                )}.`;
            }

            return `Destrua o jogador ${targetName}.`;
        }

        if (alternativeStates.length > 0) {
            return `Conquiste os territórios: ${alternativeStates.join(", ")}.`;
        }

        return "Elimine o jogador indicado pela sua missão.";
    }

    return "Tipo de missão desconhecido.";
}
