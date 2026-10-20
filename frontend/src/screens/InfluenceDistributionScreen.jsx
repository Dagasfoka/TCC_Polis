import { useEffect } from "react";
import BrazilMapSvg from "../components/BrazilMapSvg.jsx";

export default function InfluenceDistributionScreen({
    matchState,
    territories,
    players,
    me,
    partyColors,
    myTerritories,
    distributionTerritory,
    distributionAmount,
    setDistributionAmount,
    distributionAmountValue,
    maxDistributionInfluence,
    pendingDistributions,
    onSelectTerritory,
    onSaveDistribution,
    onRemoveDistribution,
    onConfirm,
}) {

    const totalPendingInfluence = Object.values(
        pendingDistributions
    ).reduce((total, amount) => total + Number(amount || 0), 0);

    const remainingInfluence = Math.max(
        0,
        Number(me?.match_influence ?? 0) - totalPendingInfluence
    );

    const savedDistributions = Object.entries(pendingDistributions);

    return (
        <div
            className="polis-distribution-overlay"
            role="dialog"
            aria-modal="true"
            aria-label="Distribuição inicial de territórios"
        >
            <section className="polis-distribution-panel">
                <img
                    className="polis-distribution-art"
                    src="/distribuicaosec.png"
                    alt="Distribuição"
                />

                <div
                    className="polis-distribution-state-card"
                    style={{
                        backgroundColor:
                            partyColors[me?.party_id] ?? "#30C067",
                        display: "flex",
                    }}
                >
                    {myTerritories.length > 0 ? (
                        <>
                            <span className="polis-distribution-state-title">
                                {distributionTerritory?.name ??
                                    "Selecione no mapa"}

                                {distributionTerritory?.region && (
                                    <>
                                        <br />
                                        <span className="polis-distribution-region">
                                            {distributionTerritory.region}
                                        </span>
                                    </>
                                )}
                            </span>

                            <div
                                className="polis-distribution-controls"
                                aria-label="Quantidade de influência"
                            >
                                <button
                                    type="button"
                                    className="polis-distribution-step"
                                    disabled={
                                        !distributionTerritory ||
                                        distributionAmountValue <= 0
                                    }
                                    onClick={() =>
                                        setDistributionAmount(
                                            Math.max(
                                                0,
                                                distributionAmountValue - 10
                                            )
                                        )
                                    }
                                    aria-label="Diminuir influência em 10"
                                >
                                    −
                                </button>

                                <input
                                    className="polis-distribution-amount"
                                    type="number"
                                    min="0"
                                    max={maxDistributionInfluence}
                                    step="10"
                                    value={distributionAmount}
                                    onChange={(event) => {
                                        const value = event.target.value;

                                        if (value === "") {
                                            setDistributionAmount("");
                                            return;
                                        }

                                        const numericValue = Number(value);

                                        setDistributionAmount(
                                            Math.min(
                                                maxDistributionInfluence,
                                                Math.max(
                                                    0,
                                                    Number.isFinite(numericValue)
                                                        ? numericValue
                                                        : 0
                                                )
                                            )
                                        );
                                    }}
                                    onBlur={() => {
                                        if (distributionAmount !== "") {
                                            setDistributionAmount(
                                                distributionAmountValue
                                            );
                                        }
                                    }}
                                    aria-label="Influência a distribuir"
                                    disabled={!distributionTerritory}
                                />

                                <button
                                    type="button"
                                    className="polis-distribution-step"
                                    disabled={
                                        !distributionTerritory ||
                                        distributionAmountValue >=
                                            maxDistributionInfluence
                                    }
                                    onClick={() =>
                                        setDistributionAmount(
                                            Math.min(
                                                maxDistributionInfluence,
                                                distributionAmountValue + 10
                                            )
                                        )
                                    }
                                    aria-label="Aumentar influência em 10"
                                >
                                    +
                                </button>

                                <button
                                    type="button"
                                    className="polis-distribution-confirm"
                                    onClick={onSaveDistribution}
                                    disabled={
                                        !distributionTerritory ||
                                        distributionAmountValue <= 0
                                    }
                                    aria-label="Salvar distribuição deste território"
                                >
                                    <img src="/confirmar.png" alt="" />
                                </button>
                            </div>

                            <div
                                className="polis-distribution-result"
                                aria-live="polite"
                            >
                                <span>Nova influência:</span>
                                <strong>
                                    {Number(
                                        distributionTerritory?.current_influence ?? 0
                                    ) + distributionAmountValue}
                                </strong>
                            </div>

                            <div className="polis-distribution-total">
                                Influência restante: {remainingInfluence}
                            </div>

                            <div className="polis-distribution-pending">
                                <h3>Distribuições salvas</h3>

                                {savedDistributions.length === 0 ? (
                                    <p>
                                        Nenhum território configurado ainda.
                                    </p>
                                ) : (
                                    <ul>
                                        {savedDistributions.map(
                                            ([territoryId, amount]) => {
                                                const territory =
                                                    myTerritories.find(
                                                        (item) =>
                                                            String(
                                                                item.territory_id
                                                            ) ===
                                                            String(territoryId)
                                                    );

                                                return (
                                                    <li key={territoryId}>
                                                        <span>
                                                            {territory?.name ??
                                                                `Território ${territoryId}`}
                                                            : {amount} de
                                                            influência
                                                        </span>

                                                        <button
                                                            type="button"
                                                            onClick={() =>
                                                                onRemoveDistribution(
                                                                    territoryId
                                                                )
                                                            }
                                                            aria-label={`Remover distribuição de ${
                                                                territory?.name ??
                                                                territoryId
                                                            }`}
                                                        >
                                                            Remover
                                                        </button>
                                                    </li>
                                                );
                                            }
                                        )}
                                    </ul>
                                )}
                            </div>

                            <button
                                type="button"
                                className="polis-distribution-finish"
                                onClick={onConfirm}
                                disabled={savedDistributions.length === 0}
                            >
                                Finalizar distribuição
                            </button>
                        </>
                    ) : (
                        <p className="polis-distribution-empty">
                            Aguardando os territórios da partida…
                        </p>
                    )}
                </div>

                <div
                    className="polis-distribution-map-wrap"
                    aria-label="Mapa dos territórios da partida"
                >
                    <BrazilMapSvg
                        territories={territories}
                        players={players}
                        partyColors={partyColors}
                        currentPlayerId={matchState?.your_player_id}
                        selectedTerritoryId={
                            distributionTerritory?.territory_id ?? null
                        }
                        selectableTerritoryIds={myTerritories.map(
                            (territory) => territory.territory_id
                        )}
                        isActionable={true}
                        onSelectTerritory={(territory) =>
                            onSelectTerritory(territory.territory_id)
                        }
                        className="polis-distribution-map"
                    />
                </div>
            </section>
        </div>
    );
}