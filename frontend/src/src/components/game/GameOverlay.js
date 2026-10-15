import { useMemo, useState, useRef } from 'react';
import Overlay from '../Overlay.js';
import { COLORS, STATES } from '../../data/Data.js';
import '../../styles/style.css';

function GameOverlays({
  gs,
  players = [],
  onAnswer,
  onClose,
  onRollDice,
  question,        // 👈 vem do backend
  diceResult,      // 👈 vem do backend
  attackResult     // 👈 vem do backend
}) {

  // fallback (caso ainda esteja rodando local)
  const q = useMemo(() => {
    if (question) return question;
    return null;
  }, [question]);

  return (
    <div>
      {overlay==='dist'&&(
        <Overlay>
          <div className="overlay-title">Sua posição inicial</div>
          <div className="overlay-sub" style={{marginBottom:14}}>Missão secreta revelada · 5 territórios distribuídos</div>
          <div style={{background:'var(--bg3)',border:'1.5px solid #2d5060',borderRadius:12,padding:'12px 14px',marginBottom:14}}>
            <div style={{display:'flex',alignItems:'center',gap:7,marginBottom:6}}>
              <span style={{color:'var(--gold)'}}>◆</span>
              <span style={{fontSize:'.58rem',fontWeight:800,color:'var(--gold)',letterSpacing:'.15em',textTransform:'uppercase',fontFamily:'Space Mono, monospace'}}>Sua missão secreta</span>
            </div>
            <div style={{fontSize:'.82rem',color:'var(--teal-l)',lineHeight:1.6}}>{gs.missions[0].text}</div>
          </div>
          <span className="lbl lbl-light" style={{marginBottom:8}}>Seus territórios iniciais</span>
          <div className="states-grid" style={{marginBottom:14}}>
            {myStates.map(sid=>{const st=STATES.find(s=>s.id===sid);return(
              <div key={sid} className="state-card">
                <div className="state-region-tag" style={{color:st.tc}}>{st.reg.slice(0,3).toUpperCase()}</div>
                <div className="state-nm">{st.name}</div>
              </div>
            );})}
          </div>
          <span className="lbl lbl-light" style={{marginBottom:8}}>Recursos iniciais</span>
          <div className="res-grid-3" style={{marginBottom:16}}>
            <div className="res-box"><span className="res-big rv-g">${gs.res.dinheiro}</span><span className="res-tiny">Dinheiro</span></div>
            <div className="res-box"><span className="res-big rv-b">{gs.res.influencia}</span><span className="res-tiny">Influência</span></div>
            <div className="res-box"><span className="res-big rv-r">{gs.res.corrupcao}%</span><span className="res-tiny">Corrupção</span></div>
          </div>
          <button className="btn btn-gold btn-full" onClick={()=>setOverlay(null)}>Começar partida →</button>
        </Overlay>
      )}

     {gs === 'question' && q && (
        <QuestionOverlay
          question={q}
          onAnswer={onAnswer}
          onClose={onClose}
        />
      )}

       {gs === 'dice' && (
       <DiceOverlay
          ctx={attackResult} // ou o estado correto
          onRoll={onRollDice}
          diceResult={diceResult}
        />
      )}

        {gs === 'result' && (
       <ResultOverlay
          ctx={attackResult}
          players={players}
          onContinue={onClose}
       />
      )}

       {gs === 'end' && (
       <EndOverlay
        gs={gameState}
        winner={gameState.winner}
        onReplay={() => {}}
        onMenu={() => {}}
      />
      )}
   
    </div>
  
    
  );
}

export default GameOverlays;

/* ─── QUESTION OVERLAY — SIM / NÃO ─────────────────── */
function QuestionOverlay({ question, action, onAnswer, onClose, flash }) {
  const [sel, setSel] = useState(null);
  const [answered, setAnswered] = useState(false);

  const ACTIONS = {
    attack: 'Atacar território vizinho',
    reinforce: 'Reforçar influência',
    collect: 'Coletar recursos',
    political: 'Ação política'
  };

  const confirm = () => {
    if (sel === null) {
      flash('Escolha Sim ou Não antes de confirmar.');
      return;
    }

    setAnswered(true);

    // backend vai decidir se está certo ou errado futuramente
    setTimeout(() => {
      onAnswer(sel); // 👈 agora só manda a resposta
    }, 900);
  };

  const correct = answered && sel === question?.c;
  const wrong = answered && sel !== question?.c;

  return (
    <Overlay onClose={!answered ? onClose : null}>
      <div className="q-ctx-bar">
        Ação: <span>{ACTIONS[action]}</span> — Responda para alterar a chance de sucesso
      </div>

      <div className="q-hdr">
        <span className="q-tag">Pergunta política</span>
        <span className="q-timer-b">0:30</span>
      </div>

      <div className="q-text">{question?.q}</div>

      {/* Botões */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 10, marginBottom: 14 }}>
        {[
          {
            label: '✓  Sim',
            val: true,
            baseColor: '#1e3a28',
            border: '#2d6040',
            activeColor: '#152e1e',
            activeBorder: 'var(--green)',
            textColor: 'var(--green)'
          },
          {
            label: '✕  Não',
            val: false,
            baseColor: '#3a1e1e',
            border: '#6a3030',
            activeColor: '#2a1010',
            activeBorder: 'var(--red)',
            textColor: 'var(--red)'
          }
        ].map(({ label, val, baseColor, border, activeColor, activeBorder, textColor }) => {
          const isSelected = sel === val;
          const isCorrectAnswer = answered && question?.c === val;
          const isWrongAnswer = answered && sel === val && val !== question?.c;

          return (
            <button
              key={String(val)}
              onClick={() => !answered && setSel(val)}
              style={{
                fontFamily: 'Nunito,sans-serif',
                fontSize: '1.05rem',
                fontWeight: 900,
                padding: '18px 12px',
                borderRadius: 14,
                border: `2px solid ${
                  isCorrectAnswer
                    ? 'var(--green)'
                    : isWrongAnswer
                    ? 'var(--red)'
                    : isSelected
                    ? activeBorder
                    : border
                }`,
                background: isCorrectAnswer
                  ? '#152e1e'
                  : isWrongAnswer
                  ? '#2a1010'
                  : isSelected
                  ? activeColor
                  : baseColor,
                color: isCorrectAnswer
                  ? 'var(--green)'
                  : isWrongAnswer
                  ? 'var(--red)'
                  : textColor,
                cursor: answered ? 'default' : 'pointer',
                transition: 'all .18s',
                transform: isSelected && !answered ? 'scale(1.03)' : 'scale(1)',
                opacity: answered && !isCorrectAnswer && !isWrongAnswer ? 0.45 : 1,
                letterSpacing: '.02em'
              }}
            >
              {label}
            </button>
          );
        })}
      </div>

      {/* Feedback */}
      {answered && (
        <div
          style={{
            background: correct ? 'rgba(21,45,30,.9)' : 'rgba(42,16,16,.9)',
            border: `1.5px solid ${correct ? 'var(--green)' : 'var(--red)'}`,
            borderRadius: 12,
            padding: '12px 14px',
            marginBottom: 14,
            animation: 'slideDown .3s cubic-bezier(.22,.68,0,1.1) both'
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: 7, marginBottom: 5 }}>
            <span style={{ fontSize: '1rem' }}>{correct ? '✓' : '✗'}</span>
            <span
              style={{
                fontSize: '.72rem',
                fontWeight: 900,
                color: correct ? 'var(--green)' : 'var(--red)',
                letterSpacing: '.1em',
                textTransform: 'uppercase',
                fontFamily: 'Space Mono,monospace'
              }}
            >
              {correct ? 'Resposta correta!' : 'Resposta incorreta!'}
            </span>
          </div>

          <div style={{ fontSize: '.78rem', color: 'var(--tx-d)', lineHeight: 1.65 }}>
            {question?.exp}
          </div>
        </div>
      )}

      <div className="impact-row">
        <span className="impact-lbl">Impacto no dado:</span>
        <div className="impact-vals">
          <div className="iv">
            <span className="iv-val" style={{ color: 'var(--green)' }}>+25%</span>
            <div className="iv-sub">se acertar</div>
          </div>
          <div className="iv">
            <span className="iv-val" style={{ color: 'var(--red)' }}>−15%</span>
            <div className="iv-sub">se errar</div>
          </div>
        </div>
      </div>

      <button className="btn btn-gold btn-full" onClick={confirm} disabled={answered}>
        {answered
          ? 'Indo para o dado...'
          : sel === null
          ? 'Escolha Sim ou Não'
          : 'Confirmar resposta →'}
      </button>
    </Overlay>
  );
}

/* ─── DICE OVERLAY ──────────────────────────────────── */
function DiceOverlay({ ctx, onRoll, diceResult }) {
  const { correct, action, bonus } = ctx;

  const [rolling, setRolling] = useState(false);
  const [displayNum, setDisplayNum] = useState(null);

  const rollRef = useRef();

  const ACTIONS = {
    attack: 'Atacar território vizinho',
    reinforce: 'Reforçar influência',
    collect: 'Coletar recursos',
    political: 'Ação política'
  };

  // ainda pode mostrar visualmente (UI)
  const threshold = Math.max(1, Math.min(10, Math.round((50 + bonus) / 10)));

  const doRoll = () => {
    if (rolling || diceResult !== null) return;

    setRolling(true);

    let count = 0;

    const interval = setInterval(() => {
      setDisplayNum(Math.floor(Math.random() * 10) + 1);
      count++;

      if (count > 18) {
        clearInterval(interval);

        // 👇 aqui NÃO decide mais o resultado
        setRolling(false);

        onRoll(); // 👈 chama backend
      }
    }, 60);

    rollRef.current = interval;
  };

  // 👇 resultado vem do backend
  const finalResult = diceResult ?? displayNum;

  const DICE_FACES = ['⚀','⚁','⚂','⚃','⚄','⚅'];
  const diceFace = finalResult
    ? DICE_FACES[Math.min(finalResult - 1, 5)]
    : '🎲';

  const success =
    diceResult !== null
      ? diceResult <= threshold
      : null;

  return (
    <Overlay>
      <div className="overlay-title">Jogue o dado!</div>
      <div className="overlay-sub" style={{ marginBottom: 14 }}>
        Role para determinar o resultado da ação
      </div>

      {/* contexto */}
      <div style={{
        background: correct ? 'rgba(21,45,30,.8)' : 'rgba(42,16,16,.8)',
        border: `1.5px solid ${correct ? 'var(--green)' : 'var(--red)'}`,
        borderRadius: 11,
        padding: '9px 13px',
        marginBottom: 14,
        display: 'flex',
        alignItems: 'center',
        gap: 9
      }}>
        <span>{correct ? '✓' : '✗'}</span>
        <div>
          <div style={{
            fontSize: '.68rem',
            fontWeight: 800,
            color: correct ? 'var(--green)' : 'var(--red)',
          }}>
            {correct
              ? `+25% → Precisa tirar ${threshold} ou menos`
              : `-15% → Precisa tirar ${threshold} ou menos`}
          </div>
          <div style={{ fontSize: '.62rem' }}>
            Ação: {ACTIONS[action]}
          </div>
        </div>
      </div>

      {/* DADO */}
      <div onClick={doRoll} style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        padding: '28px 0',
        cursor: rolling || diceResult !== null ? 'default' : 'pointer'
      }}>
        <div style={{
          fontSize: '5.5rem',
          filter: rolling ? 'blur(1px)' : 'none',
          animation: rolling ? 'shimmer .12s infinite' : 'none'
        }}>
          {diceFace}
        </div>

        {diceResult !== null && (
          <div style={{ textAlign: 'center' }}>
            <div style={{
              fontSize: '2rem',
              color: success ? 'var(--green)' : 'var(--red)'
            }}>
              {diceResult}
            </div>

            <div>
              {success ? '✓ Sucesso!' : '✗ Falhou!'}
            </div>
          </div>
        )}
      </div>

      {diceResult !== null ? (
        <button
          className="btn btn-gold btn-full"
          onClick={() => onRoll(diceResult)}
        >
          Ver resultado →
        </button>
      ) : (
        <button
          className="btn btn-teal btn-full"
          onClick={doRoll}
          disabled={rolling}
        >
          {rolling ? 'Rolando...' : '🎲 Rolar o dado'}
        </button>
      )}
    </Overlay>
  );
}

/* ─── RESULT OVERLAY ────────────────────────────────── */
function ResultOverlay({ctx,players,onContinue}){
  const {correct,action,success,bonus,roll}=ctx;
  const threshold=Math.max(1,Math.min(10,Math.round((50+bonus)/10)));
  const ACTIONS={attack:'Ataque',reinforce:'Reforço de Influência',collect:'Coleta de Recursos',political:'Ação Política'};
  return(
    <Overlay>
      <div className="result-hdr">
        <div className="result-icon">{success?'★':'✗'}</div>
        {success?<div className="result-title-w">{ACTIONS[action]} bem-sucedido!</div>:<div className="result-title-f">{ACTIONS[action]} falhou!</div>}
        <div className="result-sub">{correct?'Resposta certa → +25% de chance':'Resposta errada → −15% de chance'}</div>
      </div>
      {action==='attack'&&(
        <div className="vs-wrap">
          <div className={`vs-card${success?' winner':' loser'}`}>
            <div className="vs-big-av">{players[0].av}</div>
            <div className="vs-nm" style={{color:success?'var(--gold)':'var(--red)'}}>{players[0].name}</div>
            <div className="vs-st" style={{color:success?'#e8c070':'#7a5a5a'}}>{success?'conquistou território':'ataque repelido'}</div>
          </div>
          <div style={{fontSize:'1.1rem',fontWeight:700,color:'#5a5550'}}>×</div>
          <div className={`vs-card${success?' loser':' winner'}`}>
            <div className="vs-big-av">🧙</div>
            <div className="vs-nm" style={{color:success?'var(--red)':'var(--gold)'}}>Defensor</div>
            <div className="vs-st" style={{color:success?'#7a4a4a':'#e8c070'}}>{success?'perdeu território':'defendeu'}</div>
          </div>
        </div>
      )}
      <div className="prob-section">
        <span className="lbl lbl-light" style={{marginBottom:8}}>Resultado do dado</span>
        <div style={{display:'flex',alignItems:'center',gap:12,marginBottom:8}}>
          <div style={{fontSize:'2rem'}}>{['⚀','⚁','⚂','⚃','⚄','⚅'][Math.min(roll-1,5)]}</div>
          <div>
            <div style={{fontSize:'1.1rem',fontWeight:900,fontFamily:'Space Mono,monospace',color:success?'var(--green)':'var(--red)'}}>{roll} {success?'≤':'>'} {threshold}</div>
            <div style={{fontSize:'.62rem',color:'#6a7a80',fontFamily:'Space Mono,monospace'}}>Dado · Precisava de ≤ {threshold} para sucesso</div>
          </div>
          <div style={{marginLeft:'auto'}}>
            <span className={`badge ${success?'bg-green':'bg-red'}`}>{success?'SUCESSO':'FALHA'}</span>
          </div>
        </div>
        <div style={{display:'flex',gap:4}}>
          {Array.from({length:10},(_,i)=>{
            const n=i+1;
            return <div key={i} style={{flex:1,height:18,borderRadius:4,background:n===roll?(success?'var(--green)':'var(--red)'):n<=threshold?'rgba(201,150,58,.3)':'#1e1c1a',border:`1px solid ${n===roll?(success?'var(--green)':'var(--red)'):n<=threshold?'rgba(201,150,58,.4)':'#3a3530'}`,fontSize:'.5rem',display:'flex',alignItems:'center',justifyContent:'center',color:n===roll?'#fff':n<=threshold?'var(--gold)':'#4a4540',fontFamily:'Space Mono,monospace',fontWeight:n===roll?800:400}}>{n}</div>;
          })}
        </div>
      </div>
      <div className="changes-section">
        {action==='attack'&&<div className="chg-row"><span className="chg-l">{success?'Território conquistado':'Ataque repelido'}</span><span className={`chg-v ${success?'chg-pos':'chg-neg'}`}>{success?'+1 estado':'0'}</span></div>}
        {action==='collect'&&<div className="chg-row"><span className="chg-l">Dinheiro coletado</span><span className={`chg-v ${success?'chg-pos':'chg-neg'}`}>{success?'+$150':'+$60'}</span></div>}
        {(action==='reinforce'||action==='political')&&<div className="chg-row"><span className="chg-l">Influência ganha</span><span className={`chg-v ${success?'chg-pos':'chg-neg'}`}>{success?'+12':'+4'}</span></div>}
        <div className="chg-row"><span className="chg-l">Dinheiro gasto</span><span className="chg-v chg-neg">−$80</span></div>
        <div className="chg-row"><span className="chg-l">Corrupção</span><span className="chg-v chg-neg">+{action==='political'?5:2}%</span></div>
      </div>
      <button className="btn btn-gold btn-full" onClick={onContinue}>Continuar →</button>
    </Overlay>
  );
}

/* ─── DISCONNECT OVERLAY ────────────────────────────── */
function DisconnectOverlay({players,onVote}){
  const [voted,setVoted]=useState(false);
  const vote=e=>{setVoted(true);setTimeout(()=>onVote(e),500);};
  return(
    <Overlay>
      <div className="alert-banner">
        <div className="alert-dot"/>
        <div style={{fontSize:'.98rem',fontWeight:900}}>Jogador inativo — 2ª rodada consecutiva</div>
      </div>
      <div className="dc-player-box">
        <div className="dc-av">{players[2].av}</div>
        <div>
          <div style={{fontSize:'.88rem',fontWeight:800,color:'#d0a090',marginBottom:3}}>{players[2].name}</div>
          <div style={{fontSize:'.68rem',color:'#8a6060',fontFamily:'Space Mono, monospace'}}>Desconectado · WebSocket encerrado</div>
        </div>
      </div>
      <div style={{background:'var(--bg3)',border:'1px solid var(--div)',borderRadius:11,padding:'12px 14px',marginBottom:14}}>
        <span className="lbl lbl-light" style={{marginBottom:10}}>Votação dos jogadores restantes</span>
        <div className="vote-list">
          {[{av:'🦊',nm:'Enzo Gamer (você)',st:'sim'},{av:'🧙',nm:'Marina_K',st:'sim'},{av:'🎭',nm:'Guilherme_L',st:voted?'sim':'pend'}].map((v,i)=>(
            <div key={i} className="v-row">
              <div className="v-av">{v.av}</div>
              <span className="v-nm">{v.nm}</span>
              {v.st==='sim'&&<span className="badge bg-green">Encerrar</span>}
              {v.st==='pend'&&<span className="badge bg-gray">Aguardando...</span>}
            </div>
          ))}
        </div>
        <div className="vote-summary">{voted?'3/3':'2/3'} votos · 2 necessários para encerrar</div>
      </div>
      <div style={{display:'flex',alignItems:'center',justifyContent:'space-between',marginBottom:14}}>
        <span style={{fontSize:'.75rem',color:'var(--tx-m)'}}>Tempo para decidir</span>
        <span style={{fontFamily:'Space Mono, monospace',fontSize:'.95rem',fontWeight:700,color:'var(--red)'}}>0:42</span>
      </div>
      <div className="btn-row">
        <button className="btn btn-teal" disabled={voted} onClick={()=>vote(true)}>✓ Encerrar partida</button>
        <button className="btn btn-danger" disabled={voted} onClick={()=>vote(false)}>✕ Continuar</button>
      </div>
    </Overlay>
  );
}

/* ─── END OVERLAY ───────────────────────────────────── */
function EndOverlay({gs,winner,onReplay,onMenu}){
  const stateCount=pid=>Object.values(gs.t).filter(v=>v===pid).length;
  const sorted=[0,1,2,3].sort((a,b)=>stateCount(b)-stateCount(a));
  const podHeights=[68,48,34,22];
  return(
    <Overlay wide>
      <div className="winner-card-ov">
        <div style={{fontSize:'.58rem',letterSpacing:'.2em',textTransform:'uppercase',color:'#8a7a6a',fontFamily:'Space Mono, monospace',marginBottom:8}}>★ Partida encerrada</div>
        <div className="w-av-ov">{gs.players[winner].av}</div>
        <div className="w-name-ov">{gs.players[winner].name} venceu!</div>
        <div className="w-mission-ov">{gs.missions[winner].text}</div>
      </div>

      {/* Podium */}
      <div className="podium-row">
        {sorted.map((pid,rank)=>(
          <div key={pid} className="pod">
            <div className="pod-av" style={{width:rank===0?50:40,height:rank===0?50:40,fontSize:rank===0?28:22,borderColor:COLORS[pid]}}>{gs.players[pid].av}</div>
            <div style={{fontSize:'.65rem',fontWeight:700,color:COLORS[pid]}}>{gs.players[pid].name.slice(0,8)}</div>
            <div style={{fontSize:'.6rem',color:'#6a6056',fontFamily:'Space Mono, monospace'}}>{stateCount(pid)} est.</div>
            <div className="pod-bar" style={{height:podHeights[rank],background:COLORS[pid],opacity:.7}}/>
            <div className="pod-pos" style={{color:COLORS[pid]}}>{rank+1}º</div>
          </div>
        ))}
      </div>

      <div className="card-dark" style={{marginBottom:14}}>
        <span className="lbl lbl-light" style={{marginBottom:12}}>Missões secretas reveladas</span>
        {gs.players.map((p,i)=>(
          <div key={i} className="mission-row">
            <div className="m-av">{p.av}</div>
            <div style={{flex:1}}>
              <div className="m-top">
                <span className="m-nm">{p.name}{i===0?' (você)':''}</span>
                {i===winner?<span className="badge bg-green">✓ Concluída</span>:<span className="badge bg-red">✗ Falhou</span>}
              </div>
              <div className="m-desc">{gs.missions[i].text}</div>
            </div>
          </div>
        ))}
      </div>

      <div className="btn-row">
        <button className="btn btn-dark" onClick={onMenu}>Menu principal</button>
        <button className="btn btn-gold" style={{flex:2}} onClick={onReplay}>Jogar novamente ↺</button>
      </div>
    </Overlay>
  );
}

