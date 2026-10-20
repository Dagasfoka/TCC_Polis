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

    useEffect(() => {
        if (!distributionTerritory) {
            setDistributionAmount(0);
            return;
        }

        const territoryId = String(distributionTerritory.territory_id);

        const savedAmount = Number(
            pendingDistributions[territoryId] ?? 0
        );

        setDistributionAmount(savedAmount);
    }, [
        distributionTerritory?.territory_id,
        pendingDistributions,
        setDistributionAmount,
    ]);

    const totalPendingInfluence = Object.values(pendingDistributions)
        .reduce((total, amount) => total + Number(amount || 0), 0);
    const selectedTerritorySavedInfluence = Number(
        pendingDistributions[String(distributionTerritory?.territory_id ?? "")] ?? 0
    );
    const draftInfluenceChange = distributionTerritory
        ? distributionAmountValue - selectedTerritorySavedInfluence
        : 0;
    const remainingInfluence = Math.max(
        0,
        Number(me?.match_influence ?? 0)
            - totalPendingInfluence
            - draftInfluenceChange
    );
    const canSaveDistribution = Boolean(distributionTerritory)
        && distributionAmountValue !== selectedTerritorySavedInfluence;
    const previewTerritories = territories.map((territory) => ({
        ...territory,
        current_influence: Number(territory.current_influence ?? 0)
            + Number(pendingDistributions[String(territory.territory_id)] ?? 0),
    }));

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
                                        distributionAmountValue < 0
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
                                    step="1"
                                    value={distributionAmount}
                                    onKeyDown={(event) => {
                                        if ([".", ",", "e", "E", "+", "-"].includes(event.key)) {
                                            event.preventDefault();
                                        }
                                    }}
                                    onChange={(event) => {
                                        const value = event.target.value;

                                        if (value === "") {
                                            setDistributionAmount("");
                                            return;
                                        }

                                        if (!/^\d+$/.test(value)) {
                                            return;
                                        }

                                        const numericValue = Number(value);

                                        setDistributionAmount(
                                            Math.min(maxDistributionInfluence, numericValue)
                                        );
                                    }}
                                    onBlur={() => {
                                        if (distributionAmount === "") {
                                            setDistributionAmount(0);
                                        } else {
                                            setDistributionAmount(distributionAmountValue);
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
                                    disabled={!canSaveDistribution}
                                    aria-label="Aplicar distribuição deste território na prévia"
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
                        territories={previewTerritories}
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

                {myTerritories.length > 0 && (
                    <div className="polis-distribution-finish-container">
                        <button
                            type="button"
                            className="polis-distribution-finish"
                            onClick={onConfirm}
                            disabled={
                                remainingInfluence !== 0 ||
                                totalPendingInfluence !== Number(me?.match_influence ?? 0)
                            }
                            aria-label="Finalizar distribuição"
                        >
                            <img src="/finalizar.png" alt="Finalizar" />
                        </button>
                    </div>
                )}
            </section>
        </div>
    );
}
