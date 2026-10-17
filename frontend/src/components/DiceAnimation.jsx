export default function DiceAnimation({ diceAnimation }) {
    if (!diceAnimation) return null;

    return (
        <div
            className="polis-dice-result-overlay"
            role="status"
            aria-live="assertive"
            aria-label={diceAnimation.rolling ? "Sorteando o dado" : `${diceAnimation.success ? "Sucesso" : "Fracasso"}, resultado ${diceAnimation.roll}, CD ${diceAnimation.threshold}`}
        >
            <div className={`polis-dice-result ${diceAnimation.rolling ? "is-rolling" : diceAnimation.success ? "is-success" : "is-failure"}`}>
                <div className="polis-dice-roll">
                    <img src="/DADO.png" alt="" aria-hidden="true" />
                    <span key={`${diceAnimation.steps}-${diceAnimation.roll}`}>{diceAnimation.roll}</span>
                </div>
                <p>{diceAnimation.rolling || !diceAnimation.outcomeVisible ? "Sorteando..." : diceAnimation.success ? "SUCESSO" : "FRACASSO"}</p>
                {diceAnimation.outcomeVisible && <small>CD {diceAnimation.threshold}</small>}
            </div>
        </div>
    )
}