export default function DiceAnimation({ diceAnimation }) {
    if (!diceAnimation) return null;
    const isCritical = Number(diceAnimation.finalRoll ?? diceAnimation.roll) === 20;
    const resultLabel = isCritical ? "CRÍTICO" : diceAnimation.success ? "Sucesso" : "Fracasso";

    return (
        <div
            className="polis-dice-result-overlay"
            role="status"
            aria-live="assertive"
            aria-label={diceAnimation.rolling ? "Sorteando o dado" : `${resultLabel}, resultado ${diceAnimation.roll}, CD ${diceAnimation.threshold}`}
        >
            <div className={`polis-dice-result ${diceAnimation.rolling ? "is-rolling" : diceAnimation.success ? "is-success" : "is-failure"} ${!diceAnimation.outcomeVisible ? "is-pending" : ""} ${diceAnimation.outcomeVisible && isCritical ? "is-critical" : ""}`}>
                <div className="polis-dice-roll">
                    <img src="/DADO.png" alt="" aria-hidden="true" />
                    <span key={`${diceAnimation.steps}-${diceAnimation.roll}`}>{diceAnimation.roll}</span>
                </div>
                <p>{diceAnimation.rolling || !diceAnimation.outcomeVisible ? "Sorteando..." : isCritical ? "CRÍTICO" : diceAnimation.success ? "SUCESSO" : "FRACASSO"}</p>
                <small className={diceAnimation.outcomeVisible && isCritical ? "is-critical" : ""}>
                    CD {diceAnimation.threshold}
                </small>
            </div>
        </div>
    )
}
