import { AVATARS } from '../../data/Data.js'
import '../../styles/style.css'

function GameHUDTop({ gs, isMyTurn, player, onMenu }) {
  return (
    <div className="game-hud-top">
        <button className="btn btn-dark" style={{padding:'4px 10px',fontSize:'.68rem'}} onClick={onMenu}>Menu</button>
        <div style={{display:'flex',alignItems:'center',gap:8}}>
          <span className="hud-pill">Rodada {gs.round}/5</span>
          <span className="hud-turn">{isMyTurn?`${AVATARS[player.avatar]} Seu turno`:`Vez de ${gs.players[gs.turn].name}`}</span>
        </div>
        <span className="hud-timer">02:30</span>
      </div>
  );
}

export default GameHUDTop;
