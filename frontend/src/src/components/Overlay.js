function Overlay({onClose,children,wide,cream}){
  return(
    <div className="overlay-backdrop anim-fade" onClick={e=>{if(e.target===e.currentTarget&&onClose)onClose();}}>
      <div className={`overlay-box anim-pop${wide?' wide':''}${cream?' cream':''}`}>
        {onClose&&<button className="overlay-close" onClick={onClose}>✕</button>}
        {children}
      </div>
    </div>
  );
}

export default Overlay;