export default function LastActionResult({ result }) {
    if (!result) {
        return (
            <section className="polis-last-action-section">
                <div className="polis-last-action-card">
                    <h2>Última ação</h2>

                    <p className="polis-last-action-empty">
                        Nenhuma ação realizada ainda.
                    </p>
                </div>
            </section>
        );
    }

    const formatValue = (value) => {
        const number = Number(value ?? 0);

        if (number > 0) {
            return `+${number}`;
        }

        return String(number);
    };

    return (
        <section className="polis-last-action-section">

            <div
                className={[
                    "polis-last-action-card",
                    result.success
                        ? "polis-action-success"
                        : "polis-action-failure",
                ].join(" ")}
            >

                <div className="polis-last-action-header">

                    <div>
                        <span className="polis-last-action-label">
                            Última ação
                        </span>

                        <h2>
                            {result.title ?? "Ação realizada"}
                        </h2>
                    </div>

                    <span className="polis-last-action-status">
                        {result.success
                            ? "SUCESSO"
                            : "FALHA"}
                    </span>

                </div>


                <div className="polis-last-action-content">

                    {result.type && (
                        <p>
                            <span>Tipo:</span>{" "}
                            {result.type}
                        </p>
                    )}


                    {result.territory_name && (
                        <p>
                            <span>Território:</span>{" "}
                            {result.territory_name}
                        </p>
                    )}


                    {result.response && (
                        <p className="polis-last-action-response">
                            {result.response}
                        </p>
                    )}


                    <div className="polis-last-action-values">

                        {Number(result.influence_generated ?? 0) !== 0 && (
                            <div>
                                <span>Influência</span>

                                <span>
                                    {formatValue(
                                        result.influence_generated
                                    )}
                                </span>
                            </div>
                        )}


                        {Number(result.money_generated ?? 0) !== 0 && (
                            <div>
                                <span>Dinheiro</span>

                                <span>
                                    {formatValue(
                                        result.money_generated
                                    )}
                                </span>
                            </div>
                        )}


                        {Number(result.corruption_generated ?? 0) !== 0 && (
                            <div>
                                <span>Corrupção</span>

                                <span>
                                    {formatValue(
                                        result.corruption_generated
                                    )}
                                </span>
                            </div>
                        )}

                    </div>


                    <div className="polis-last-action-details">

                        {result.conquered === true && (
                            <p>
                                ✓ Território conquistado
                            </p>
                        )}


                        {result.question_was_correct === true && (
                            <p>
                                ✓ Pergunta respondida corretamente
                            </p>
                        )}


                        {result.question_was_correct === false && (
                            <p>
                                ✕ Pergunta respondida incorretamente
                            </p>
                        )}

                    </div>

                </div>

            </div>

        </section>
    );
}