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
    distributionConfirmed,
    setDistributionConfirmed,
    distributionAmount,
    setDistributionAmount,
    distributionAmountValue,
    maxDistributionInfluence,
    setDistributionTerritoryId,
    onConfirm,
}) {
    useEffect(() => {
        if (distributionTerritory?.territory_id) {
            setDistributionAmount(0);
        }
    }, [distributionTerritory?.territory_id, maxDistributionInfluence, setDistributionAmount]);

    return (
        <div className="polis-distribution-overlay" role="dialog" aria-modal="true" aria-label="Distribuição inicial de territórios">
            <section className="polis-distribution-panel">
                <img className="polis-distribution-art" src="/distribuicaosec.png" alt="Distribuição" />

                <div
                    className="polis-distribution-state-card"
                    style={{
                        backgroundColor: partyColors[me?.party_id] ?? "#30C067",
                        display: distributionConfirmed ? "none" : "flex",
                    }}
                >
                    {myTerritories.length > 0 ? (
                        <>
                            <span className="polis-distribution-state-title">
                                {distributionTerritory?.name ?? "Selecione no mapa"}
                                {distributionTerritory?.region && (
                                    <>
                                        <br />
                                        <span className="polis-distribution-region">
                                            {distributionTerritory.region}
                                        </span>
                                    </>
                                )}
                            </span>
                            <div className="polis-distribution-controls" aria-label="Quantidade de influência">
                                <button
                                    type="button"
                                    className="polis-distribution-step"
                                    disabled={distributionAmountValue <= 0}
                                    onClick={() =>
                                        setDistributionAmount(
                                            Math.max(0, distributionAmountValue - 10)
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
                                        setDistributionAmount(event.target.value);
                                    }}
                                    onBlur={() => setDistributionAmount(distributionAmountValue)}
                                    aria-label="Influência a distribuir"
                                />
                                <button
                                    type="button"
                                    className="polis-distribution-step"
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
                                    onClick={onConfirm}
                                    disabled={distributionAmountValue <= 0}
                                    aria-label="Confirmar distribuição"
                                >
                                    <img src="/confirmar.png" alt="" />
                                </button>
                            </div>
                            <div className="polis-distribution-result" aria-live="polite">
                                <span>Nova influência:</span>
                                <strong>
                                    {Number(distributionTerritory?.current_influence ?? 0) + distributionAmountValue}
                                </strong>
                            </div>
                            <div className="polis-distribution-total">
                                Restante: {Math.max(0, maxDistributionInfluence - distributionAmountValue)}
                            </div>
                        </>
                    ) : (
                        <p className="polis-distribution-empty">Aguardando os territórios da partida…</p>
                    )}
                </div>

                <div className="polis-distribution-map-wrap" aria-label="Mapa dos territórios da partida">
                    <BrazilMapSvg
                        territories={territories}
                        players={players}
                        partyColors={partyColors}
                        currentPlayerId={matchState?.your_player_id}
                        selectedTerritoryId={distributionTerritory?.territory_id ?? null}
                        selectableTerritoryIds={myTerritories.map((territory) => territory.territory_id)}
                        isActionable={true}
                        onSelectTerritory={(territory) => {
                            setDistributionTerritoryId(territory.territory_id);
                            setDistributionConfirmed(false);
                        }}
                        className="polis-distribution-map"
                    />
                </div>
            </section>
        </div>
    )
}
