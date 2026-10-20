import { TERRITORY_PATHS } from "./brazilTerritoryPaths.js";

function getTerritoryBounds(path) {
    if (!path) return null;

    const tokens = path.match(/[MLHVZ]|-?(?:\d+\.?\d*|\.\d+)/g) ?? [];
    let command = "";
    let x = 0;
    let y = 0;
    const xs = [];
    const ys = [];

    for (let index = 0; index < tokens.length;) {
        if (/^[A-Za-z]$/.test(tokens[index])) {
            command = tokens[index++];
            if (command === "Z") continue;
        }

        if (command === "M" || command === "L") {
            x = Number(tokens[index++]);
            y = Number(tokens[index++]);
            xs.push(x);
            ys.push(y);
            if (command === "M") command = "L";
        } else if (command === "H") {
            x = Number(tokens[index++]);
            xs.push(x);
            ys.push(y);
        } else if (command === "V") {
            y = Number(tokens[index++]);
            xs.push(x);
            ys.push(y);
        } else {
            return null;
        }
    }

    if (!xs.length) return null;
    return {
        x: Math.min(...xs),
        y: Math.min(...ys),
        width: Math.max(...xs) - Math.min(...xs),
        height: Math.max(...ys) - Math.min(...ys),
    };
}

export default function LastActionResult({ result, onClose, players = [], partyColors = {} }) {
    if (!result) return null;

    const money = Number(result.money_generated ?? 0);
    const corruption = Number(result.corruption_generated ?? 0);
    const previousOwner = players.find(
        (player) => String(player.player_id) === String(result.old_owner_id ?? result.previous_owner_id)
    );
    const nextOwner = players.find(
        (player) => String(player.player_id) === String(result.new_owner_id)
    );
    const getOwnerColor = (owner, partyId) =>
        partyColors[owner?.party_id ?? partyId] ?? "#777777";
    const previousInfluence = result.old_current_influence ?? result.previous_influence;
    const nextInfluence = result.new_current_influence ?? result.new_influence;
    const territoryId = result.territory_id ?? result.target_territory_id;
    const territoryPath = TERRITORY_PATHS[territoryId];
    const territoryBounds = getTerritoryBounds(territoryPath);

    const formatValue = (value) => {
        const number = Number(value ?? 0);
        return number > 0 ? `+${number}` : String(number);
    };

    const renderTerritory = (owner, partyId, influence, label) => {
        if (!territoryPath || !territoryBounds) {
            return (
                <div
                    className="polis-action-result-state-marker"
                    aria-label={`${label}: influência ${influence ?? "não informada"}`}
                >
                    <span className="polis-action-result-influence-value">{influence ?? "—"}</span>
                    <span
                        className="polis-action-result-state-fallback"
                        style={{ backgroundColor: getOwnerColor(owner, partyId) }}
                    />
                </div>
            );
        }

        const padding = Math.max(3, Math.min(territoryBounds.width, territoryBounds.height) * 0.025);
        return (
            <div
                className="polis-action-result-state-marker"
                aria-label={`${label}: influência ${influence ?? "não informada"}`}
            >
                <span className="polis-action-result-influence-value">{influence ?? "—"}</span>
                <svg
                    className="polis-action-result-state-shape"
                    viewBox={`${territoryBounds.x - padding} ${territoryBounds.y - padding} ${territoryBounds.width + padding * 2} ${territoryBounds.height + padding * 2}`}
                    role="img"
                    aria-hidden="true"
                >
                    <path
                        d={territoryPath}
                        fill={getOwnerColor(owner, partyId)}
                        stroke="#17130f"
                        strokeWidth={2.8}
                        strokeLinejoin="round"
                    />
                </svg>
            </div>
        );
    };

    return (
        <div
            className="polis-action-result-overlay"
            role="dialog"
            aria-modal="true"
            aria-label="Resultado da ação"
            onClick={onClose}
        >
            <div
                className="polis-last-action-card polis-action-result-card"
                onClick={(event) => event.stopPropagation()}
            >
                <img
                    className="polis-action-result-screen-title"
                    src="/resultado-titulo.png"
                    alt="Resultado da Ação"
                />
                <div className={`polis-action-result-outcome ${result.success ? "is-success" : "is-failure"}`}>
                    <img
                        src={result.success ? "/sucesso.png" : "/fracasso.png"}
                        alt={result.success ? "Sucesso" : "Fracasso"}
                    />
                </div>

                <section className="polis-action-result-action-section">
                    <span className="polis-action-result-section-heading">
                        {result.territory_name ?? "Ação"}
                    </span>
                    <h2 className="polis-action-result-action-title">
                        {result.title ?? "Ação realizada"}
                    </h2>
                    {result.response && (
                        <p className="polis-action-result-description">
                            {result.response}
                        </p>
                    )}
                </section>

                <section className="polis-action-result-state-change" aria-label="Estado antes e depois da ação">
                    <div className="polis-action-result-state-flow">
                        {renderTerritory(previousOwner, result.old_party_id, previousInfluence, "Antes da ação")}
                        <span className="polis-action-result-arrow" aria-hidden="true">→</span>
                        {renderTerritory(nextOwner, result.new_party_id, nextInfluence, "Depois da ação")}
                    </div>
                </section>

                <section className="polis-action-result-status-section">
                    <div className="polis-last-action-values polis-action-result-values">
                        {money !== 0 && (
                            <div
                                className={money > 0 ? "result-money-positive" : "result-money-negative"}
                                aria-label={`Dinheiro R$ ${formatValue(money)}`}
                            >
                                <span className="result-value-number">R$ {formatValue(money)}</span>
                            </div>
                        )}
                        {corruption !== 0 && (
                            <div className="result-corruption" aria-label={`Corrupção ${formatValue(corruption)}%`}>
                                <span className="result-value-number">{formatValue(corruption)}%</span>
                            </div>
                        )}
                    </div>
                </section>

                <button
                    type="button"
                    className="polis-action-result-close"
                    onClick={onClose}
                    aria-label="Continuar"
                >
                    <img className="continue-normal" src="/CONTINUARPRETO.png" alt="Continuar" />
                    <img className="continue-hover" src="/CONTINUAR.png" alt="" aria-hidden="true" />
                </button>
            </div>
        </div>
    );
}
