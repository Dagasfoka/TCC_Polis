export default function GameNotice({ notice }) {
  if (!notice) return null;

  return (
    <div
      className="polis-game-notice-backdrop"
      aria-live="polite"
      aria-atomic="true"
    >
      <p
        key={notice.id}
        className={`polis-game-notice polis-game-notice-${notice.kind}`}
        role="status"
      >
        {notice.message}
      </p>
    </div>
  );
}