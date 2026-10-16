import '../../styles/style.css'

function GameSidebar({
  gs,
  playerId, // 👈 novo
  COLORS,
  isMyTurn,
  stateCount,
  ACTIONS,
  doAction
}) {
  return (
      <div className="map-sidebar">
          <div className="side-section">
            <span className="lbl lbl-light" style={{marginBottom:8}}>Recursos</span>
            <div className="res-row"><span className="res-lbl">Dinheiro</span><span className="res-val rv-g">${gs.res.dinheiro}</span></div>
            <div className="res-row"><span className="res-lbl">Influência</span><span className="res-val rv-b">{gs.res.influencia}</span></div>
            <div className="res-row"><span className="res-lbl">Corrupção</span><span className="res-val rv-r">{gs.res.corrupcao}%</span></div>
            <div className="prog-wrap" style={{marginTop:5}}>
              <div className="prog-fill" style={{width:`${gs.res.corrupcao}%`,background:'var(--red)'}}/>
            </div>
          </div>

          <div className="side-section">
            <span className="lbl lbl-light" style={{marginBottom:8}}>Jogadores</span>
            {gs.players.map((p,i)=>(
              <div key={i} className="p-mini">
                <div className={`p-mini-av${i === playerId?' me':''}`} style={{borderColor:COLORS[i]}}>{p.av}</div>
                <div style={{flex:1}}>
                  <div className="p-mini-name">{p.name.slice(0,9)}{i===0?' ★':''}</div>
                  <div className="p-mini-count">{stateCount(i)} estados</div>
                </div>
                <div className="p-mini-dot" style={{background:COLORS[i]}}/>
              </div>
            ))}
          </div>

          <div className="side-section" style={{opacity:isMyTurn?1:.5}}>
            <span className="lbl lbl-light" style={{marginBottom:8}}>{gs.sel?`Ações — ${gs.sel}`:'Selecione um estado'}</span>
            {ACTIONS.map(a=>(
              <button key={a.id} className="act-mini-btn btn-full" style={{marginBottom:5,opacity:gs.sel?1:.6}} onClick={()=>doAction(a.id)}>
                <span>{a.icon}</span>{a.label}
              </button>
            ))}
          </div>
        </div>       
  );
}

export default GameSidebar;
