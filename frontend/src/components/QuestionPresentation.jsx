import { useEffect, useState } from "react";
const QUESTION_SUBJECT_LABELS = {
    philosophy: "Filosofia",
    sociology: "Sociologia",
    geography: "Geografia",
    history: "História",
};

const QUESTION_DIFFICULTY_LABELS = {
    easy: "Fácil",
    medium: "Médio",
    hard: "Difícil",
};

export default function QuestionPresentation({
    question,
    targetName,
    onAnswer,
    onDismiss,
    feedback = null,
    isDemo = false,
}) {

    const [selectedAnswer, setSelectedAnswer] = useState(null);
    const [remainingSeconds, setRemainingSeconds] = useState(30);

    useEffect(() => {
        if (feedback) setRemainingSeconds(30);
    }, [Boolean(feedback)]);

    useEffect(() => {
        if (remainingSeconds <= 0 || (selectedAnswer !== null && !feedback)) return undefined;

        const timeoutId = window.setTimeout(() => {
            setRemainingSeconds((current) => Math.max(0, current - 1));
        }, 1000);

        return () => window.clearTimeout(timeoutId);
    }, [feedback, remainingSeconds, selectedAnswer]);

    if (!question) return null;

    const timerMinutes = String(Math.floor(remainingSeconds / 60)).padStart(2, "0");
    const timerSeconds = String(remainingSeconds % 60).padStart(2, "0");

    function handleAnswer(letter) {
        if (isDemo) {
            setSelectedAnswer(letter);
            return;
        }
        setSelectedAnswer(letter);
        onAnswer(letter);
    }

    const answerReview = feedback ?? (
        isDemo && selectedAnswer !== null
            ? { selectedAnswer, correctAnswer: question.answer }
            : null
    );
    const reviewedSelection = answerReview?.selectedAnswer ?? selectedAnswer;
    const selectionIsCorrect = reviewedSelection === answerReview?.correctAnswer;

    return (
        <div
            className="polis-question-preview-overlay"
            role="dialog"
            aria-modal="true"
            aria-label={isDemo ? "Tela demonstrativa de pergunta" : "Pergunta da partida"}
            onClick={isDemo || feedback ? onDismiss : undefined}
        >
            <section
                className="polis-question-preview-box"
                onClick={isDemo || feedback ? (event) => event.stopPropagation() : undefined}
            >
                <img className="polis-question-preview-bg" src="/areapergunta.png" alt="" />
                <div className="polis-question-preview-top-row">
                    {targetName && (
                        <span className="polis-question-preview-target">Alvo: {targetName}</span>
                    )}
                    <div
                        className="polis-question-preview-timer"
                        role="timer"
                        aria-label={`Tempo restante: ${timerMinutes}:${timerSeconds}`}
                    >
                        {timerMinutes}:{timerSeconds}
                    </div>
                </div>
                <div className="polis-question-preview-tags">
                    <span>{QUESTION_SUBJECT_LABELS[String(question.subject ?? "").toLowerCase()] ?? question.subject}</span>
                    {question.difficulty && (
                        <span>{QUESTION_DIFFICULTY_LABELS[String(question.difficulty).toLowerCase()] ?? question.difficulty}</span>
                    )}
                    <span className="polis-question-preview-chance-tag">
                        Chance de sucesso: +20%
                    </span>
                </div>
                <div className="polis-question-preview-content">
                    <div className="polis-question-preview-main">
                        <div className="polis-question-preview-body">
                            <p className="polis-question-preview-title">
                                {question.question_id ?? 1}) {question.exam_board ? `(${question.exam_board})` : ""}
                            </p>
                            <p>{question.description}</p>
                        </div>
                        <div className="polis-question-preview-answers">
                            {Object.entries(question.options ?? {}).map(([letter, text]) => (
                                <button
                                    type="button"
                                    key={letter}
                                    onClick={() => handleAnswer(letter)}
                                    disabled={selectedAnswer !== null || Boolean(feedback)}
                                    className={answerReview && letter === reviewedSelection
                                        ? selectionIsCorrect ? "is-correct" : "is-incorrect"
                                        : ""}
                                >
                                    {letter}) {text}
                                </button>
                            ))}
                        </div>
                    </div>
                    {question.explanation && (Boolean(feedback) || (isDemo && selectedAnswer !== null)) && (
                        <div className="polis-question-preview-explanation">
                            <p>Explicação:</p>
                            <span>{question.explanation}</span>
                        </div>
                    )}
                    <div>
                        {(feedback || (isDemo && selectedAnswer !== null)) && (
                            <button
                                type="button"
                                className="polis-question-preview-continue"
                                onClick={onDismiss}
                                aria-label="Continuar"
                            >
                                <img src="/CONTINUAR.png" alt="" />
                            </button>
                        )}
                    </div>
                </div>
            </section>
        </div>
    );
}
