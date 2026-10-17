export default function TerritoryActions({
    selectedTerritory,
    isMyTurn,
    availableActions,
    onChooseAction,
    onClose,
}) {
    if (!selectedTerritory) return null;

    return (
        (
            <div className="polis-choice-overlay">
                <section className="polis-choice-board" aria-label="Escolhas do território">
                    <header className="polis-choice-board-header">
                        <div className="polis-choice-territory">
                            <h2>
                                {selectedTerritory.name &&
                                    selectedTerritory.name !== selectedTerritory.territory_id
                                    ? `${selectedTerritory.name} (${selectedTerritory.territory_id})`
                                    : selectedTerritory.territory_id}
                            </h2>
                            <span>{selectedTerritory.region ?? "-"}</span>
                        </div>
                        <div className="polis-choice-influence">
                            <span>Influência do estado</span>
                            <span>{selectedTerritory.current_influence ?? 0}</span>
                        </div>
                    </header>

                    {isMyTurn ? (
                        <div className="polis-choice-cards">
                            {availableActions.length === 0 && (
                                <p className="polis-no-choice">Nenhuma ação disponível.</p>
                            )}
                            {availableActions.slice(0, 4).map((option) => (
                                <button
                                    type="button"
                                    className="polis-choice-card"
                                    key={option.action_id}
                                    onClick={() =>  onChooseAction(option.action_id, option.action_type)}
                                >
                                    <span className="polis-choice-card-title">
                                        <strong>{option.title}</strong>
                                    </span>
                                    <span className="polis-choice-card-risk">
                                        {({
                                            low: "Risco baixo",
                                            medium: "Risco médio",
                                            high: "Risco alto",
                                            insane: "Risco insano",
                                        })[option.risk_level] ?? option.risk_level ?? "Risco não informado"}
                                    </span>
                                    {option.description && (
                                        <span className="polis-choice-card-description">{option.description}</span>
                                    )}
                                    <span className="polis-choice-card-status">
                                        {(option.influence ?? option.influence_generated) !== undefined && (
                                            <span className="polis-choice-gain-influence">+{option.influence ?? option.influence_generated} influência</span>
                                        )}
                                        {option.money !== undefined && Number(option.money) !== 0 && (
                                            <span className="polis-choice-gain-money">+{option.money}$</span>
                                        )}
                                        {option.corruption !== undefined && Number(option.corruption) !== 0 && (
                                            <span className="polis-choice-gain-corruption">
                                                {Number(option.corruption) > 0 ? "+" : ""}{option.corruption}% corrupção
                                            </span>
                                        )}
                                    </span>
                                    {option.cost !== undefined && option.cost !== null && (
                                        <span className="polis-choice-card-cost">
                                            <span className="polis-choice-card-cost-value">-{option.cost}$</span>
                                        </span>
                                    )}
                                    {option.success_chance !== undefined && option.success_chance !== null && (
                                        <span className="polis-choice-success">
                                            <img className="polis-choice-die-icon" src="/DADO.png" alt="Dado" />
                                            <span>{option.success_chance}</span>
                                        </span>
                                    )}
                                </button>
                            ))}
                        </div>
                    ) : (
                        <p className="polis-not-your-turn">Aguarde sua vez para realizar uma ação.</p>
                    )}
                </section>
                <button
                    type="button"
                    className="polis-choice-back"
                    onClick={onClose}
                >
                    Voltar
                </button>
            </div>
        )
    );
}