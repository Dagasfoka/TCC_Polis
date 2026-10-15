import { STATES } from '../../data/Data.js'
import '../../styles/style.css'

export default function GameBottomHud({
  gs,
  isMyTurn,
  endTurn,
  flash,
  setOverlay
}) {
  return (
    <div className="game-hud-bot">
      <div>
        {gs.sel ? (
          <span className="sel-state-chip">
            Estado selecionado: <span>{STATES.find(s => s.id === gs.sel)?.name}</span>
          </span>
        ) : (
          <span style={{
            fontSize: '.72rem',
            color: '#5a5550',
            fontFamily: 'Space Mono, monospace'
          }}>
            Clique em um de seus estados no mapa
          </span>
        )}
      </div>

      <div style={{ display: 'flex', gap: 8 }}>
        <button
          className="btn btn-danger"
          style={{ fontSize: '.72rem', padding: '6px 12px' }}
          onClick={() => setOverlay('disconnect')}
        >
          ⚠ Reportar
        </button>

        <button
          className="btn btn-gold"
          style={{ fontSize: '.8rem', padding: '7px 18px' }}
          onClick={isMyTurn ? endTurn : () => flash('Aguarde seu turno.')}
          disabled={!isMyTurn}
        >
          {isMyTurn ? 'Encerrar turno →' : 'Aguardando...'}
        </button>
      </div>
    </div>
  );
}
