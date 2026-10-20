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

    const formatValue = (value) => {
        const number = Number(value ?? 0);
        return number > 0 ? `+${number}` : String(number);
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

                <div className="polis-last-action-header">
                    <div className="polis-action-result-title-block">
                        {result.territory_name && (
                            <span className="polis-action-result-territory">
                                {result.territory_name}
                            </span>
                        )}
                        <h2 className="polis-action-result-action-title">
                            {result.title ?? "Ação realizada"}
                        </h2>
                    </div>

                    <button
                        type="button"
                        className="polis-action-result-close"
                        onClick={onClose}
                        aria-label="Sair do resultado da ação"
                    >
                        Sair
                    </button>
                </div>

                <div className="polis-last-action-content">
                    {(result.description ?? result.response) && (
                        <p className="polis-action-result-description">
                            {result.description ?? result.response}
                        </p>
                    )}

                    <div className="polis-action-result-outcome">
                        <img
                            className="polis-action-result-stamp"
                            src={result.success ? "/sucesso.png" : "/fracasso.png"}
                            alt={result.success ? "Sucesso" : "Fracasso"}
                        />
                    </div>

                    <div className="polis-action-result-state-change" aria-label="Estado antes e depois da ação">
                        <span className="polis-action-result-state-heading">Estado</span>
                        <div className="polis-action-result-state-flow">
                            <span className="polis-action-result-party-ball" style={{ backgroundColor: getOwnerColor(previousOwner, result.old_party_id) }}>
                                {previousInfluence ?? "—"}
                            </span>
                            <span className="polis-action-result-arrow" aria-hidden="true">→</span>
                            <span className="polis-action-result-party-ball" style={{ backgroundColor: getOwnerColor(nextOwner, result.new_party_id) }}>
                                {nextInfluence ?? "—"}
                            </span>
                        </div>
                    </div>

                    <div className="polis-last-action-values polis-action-result-values">
                        {money !== 0 && (
                            <div className={money > 0 ? "result-money-positive" : "result-money-negative"}>
                                <span>Dinheiro</span>
                                <span className="result-value-number">{formatValue(money)}</span>
                            </div>
                        )}
                        {corruption !== 0 && (
                            <div className="result-corruption">
                                <span>Corrupção</span>
                                <span className="result-value-number">{formatValue(corruption)}</span>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}
