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
        <div className="polis-mission-modal-overlay">
            <section
                className="polis-mission-modal"
                role="dialog"
                aria-modal="true"
                aria-labelledby="mission-modal-title"
            >
                <h2 id="mission-modal-title">Sua missão secreta</h2>

                <p>{formatMission(mission, players)}</p>

                {remainingSeconds !== null ? (
                    <p>
                        {remainingSeconds > 0
                            ? `A distribuição começa em ${remainingSeconds}s`
                            : "Aguardando início da distribuição…"}
                    </p>
                ) : (
                    <button type="button" onClick={onClose}>
                        Fechar
                    </button>
                )}
            </section>
        </div>
    );
}