import { useEffect, useState } from "react";
import { formatMission } from "../utils/missionUtils.js";

export default function MissionModal({
    mission,
    players,
    endsAt,
    onClose,
}) {
    const [now, setNow] = useState(() => Date.now());

    useEffect(() => {
        if (endsAt == null) return;

        setNow(Date.now());

        const intervalId = window.setInterval(() => {
            setNow(Date.now());
        }, 250);

        return () => window.clearInterval(intervalId);
    }, [endsAt]);

    const remainingSeconds = endsAt == null
        ? null
        : Math.max(0, Math.ceil((endsAt * 1000 - now) / 1000));

    return (
        <aside
            className="polis-mission-card polis-mission-right polis-mission-consult"
            aria-label="Sua missão secreta"
        >
            <img
                className="polis-mission-art"
                src="/missaosec.png"
                alt="Missão Secreta"
            />

            <div className="polis-mission-copy">
                <p>{formatMission(mission, players)}</p>

                {remainingSeconds !== null ? (
                    <p className="polis-mission-countdown">
                        {remainingSeconds > 0
                            ? `Distribuição em ${remainingSeconds}s`
                            : "Aguardando distribuição…"}
                    </p>
                ) : (
                    <button type="button" onClick={onClose}>
                        Fechar
                    </button>
                )}
            </div>
        </aside>
    );
}