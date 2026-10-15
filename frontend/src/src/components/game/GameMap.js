function GameMap({
  gs,
  playerId, 
  MAP_POS,
  COLORS,
  ownerColor,
  isMyTurn,
  selectState,
  setGs
}) {
  return (
    <div
      className="map-canvas"
      onClick={e=>{
        if(e.target===e.currentTarget){
          setGs(g=>({...g,sel:null}));
        }
      }}
    >

       <svg viewBox="0 0 290 215" xmlns="http://www.w3.org/2000/svg" style={{width:'100%',height:'100%',maxHeight:'100%'}}>
            {Object.entries(MAP_POS).map(([sid,{x,y,w,h}])=>{
              const owner=gs.t[sid];
              const isSel=gs.sel===sid;
              const isMine = owner === playerId;
              const col=owner!==null?ownerColor(owner):'#222018';
              const stroke=isSel?'#fff':isMine?'#e8c070':'#3a3530';
              const sw=isSel?2.5:isMine?2:1.5;
              return(
                    <g key={sid} 
                    
                    onClick={() => {
                      if (isMyTurn && isMine) {
                        selectState(sid);
                    }
                  }} style={{cursor:isMyTurn&&isMine?'pointer':'default',transition:'opacity .2s'}}>
                  <rect x={x} y={y} width={w} height={h} rx={5} fill={col} stroke={stroke} strokeWidth={sw} opacity={isSel?1:.88}/>
                  {isSel&&<rect x={x} y={y} width={w} height={h} rx={5} fill="rgba(255,255,255,.08)" stroke="#fff" strokeWidth={2.5} strokeDasharray="4,2"/>}
                  <text x={x+w/2} y={y+h/2+3} textAnchor="middle" fontSize={7} fill={isMine?'#fff':'#c0b0a0'} fontFamily="Space Mono" fontWeight={isSel?'bold':'normal'}>{sid}</text>
                </g>
              );
            })}
            {gs.players.map((p,i)=>(
              <g key={i}>
                <rect x={5+i*68} y={202} width={7} height={7} rx={2} fill={COLORS[i]}/>
                <text x={15+i*68} y={209} fontSize={6} fill="#a0a098" fontFamily="Space Mono">{p.name.slice(0,7)}</text>
              </g>
            ))}
          </svg>
     
    </div>
  );
}

export default GameMap;