import { useEffect, useState } from "react";
import { formatMission } from "../utils/missionUtils.js";

export default function MissionModal({
    mission,
    players,
    endsAt,
    isOpen = false,
    isRevealing = false,
    showLargeMission = false,
    onClose,
    onCloseLarge,
    onOpen,
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

    const missionText = formatMission(mission, players);
    const revealVisible = isRevealing || showLargeMission;
    const toggleDrawer = () => {
        if (revealVisible) return;
        (isOpen ? onClose : onOpen)?.();
    };

    return (
        <>
            <aside
                className={`polis-mission-card polis-mission-right polis-mission-consult${isOpen ? " is-open" : ""}${revealVisible ? " is-locked" : ""}`}
                aria-label="Sua missão secreta"
                aria-expanded={isOpen}
                aria-disabled={revealVisible}
                onClick={toggleDrawer}
                role="button"
                tabIndex={revealVisible ? -1 : 0}
                onKeyDown={(event) => {
                    if (event.key === "Enter" || event.key === " ") {
                        event.preventDefault();
                        toggleDrawer();
                    }
                }}
            >
                <img className="polis-mission-art" src="/missaosecreta.png" alt="Missão Secreta" />
                <div className="polis-mission-copy">
                    <p>{missionText}</p>
                </div>
            </aside>

            {revealVisible && (
                <div className="polis-mission-reveal-overlay" role="dialog" aria-modal="true" aria-label="Leia sua missão secreta">
                    <div className="polis-mission-reveal-paper">
                        <img src="/missaosecreta.png" alt="" />
                        <div className="polis-mission-reveal-copy">
                            <p>{missionText}</p>
                            {isRevealing && (
                                <p className="polis-mission-countdown">
                                    {remainingSeconds > 0
                                        ? `Leia sua missão: ${remainingSeconds}s`
                                        : "Preparando a partida…"}
                                </p>
                            )}
                        </div>
                        {showLargeMission && !isRevealing && (
                            <button
                                type="button"
                                className="polis-mission-reveal-close"
                                onClick={onCloseLarge}
                            >
                                Fechar
                            </button>
                        )}
                    </div>
                </div>
            )}
        </>
    );
}
