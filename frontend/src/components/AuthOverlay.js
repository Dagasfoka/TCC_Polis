import { useState } from 'react';
import Overlay from './Overlay.js';

function AuthOverlay({ mode, onSuccess, onClose, flash }) {
  const [tab, setTab] = useState(mode);
  const [email, setEmail] = useState('');
  const [senha, setSenha] = useState('');
  const [senha2, setSenha2] = useState('');
  const [name, setName] = useState('');

  // 🔐 LOGIN (simples por enquanto)
  const doLogin = async () => {
    if (!email || !senha) {
      flash('Preencha e-mail e senha.');
      return;
    }

    try {
      // ⚠️ você ainda NÃO tem rota de login real
      // então vamos simular buscando player por nome/email

      const username = name || email.split('@')[0];

      const res = await fetch('http://localhost:8000/players', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username })
      });

      const player = await res.json();

      onSuccess(player); // 🔥 AGORA retorna objeto real
    } catch (err) {
      flash('Erro ao conectar com servidor.');
    }
  };

  // 🧾 CADASTRO
  const doCad = async () => {
    if (!name || !email || !senha || !senha2) {
      flash('Preencha todos os campos.');
      return;
    }

    if (senha !== senha2) {
      flash('Senhas não coincidem.');
      return;
    }

    try {
      const res = await fetch('http://localhost:8000/players', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: name })
      });

      const player = await res.json();

      flash('Conta criada!');
      setTimeout(() => onSuccess(player), 500);

    } catch (err) {
      flash('Erro ao criar conta.');
    }
  };

  return (
    <Overlay onClose={onClose} cream>
      <div style={{ display: 'flex', justifyContent: 'center', gap: 6, marginBottom: 16 }}>
        {['login', 'cadastro'].map(t => (
          <button
            key={t}
            onClick={() => setTab(t)}
          >
            {t === 'login' ? 'Login' : 'Cadastro'}
          </button>
        ))}
      </div>

      <div className="overlay-title dark">
        {tab === 'login' ? 'Login' : 'Cadastro'}
      </div>

      {tab === 'cadastro' && (
        <div className="field">
          <label>Nome</label>
          <input value={name} onChange={e => setName(e.target.value)} />
        </div>
      )}

      <div className="field">
        <label>E-mail</label>
        <input value={email} onChange={e => setEmail(e.target.value)} />
      </div>

      <div className="field">
        <label>Senha</label>
        <input type="password" value={senha} onChange={e => setSenha(e.target.value)} />
      </div>

      {tab === 'cadastro' && (
        <div className="field">
          <label>Repita a senha</label>
          <input type="password" value={senha2} onChange={e => setSenha2(e.target.value)} />
        </div>
      )}

      <div className="btn-row">
        <button onClick={onClose}>Cancelar</button>

        <button onClick={tab === 'login' ? doLogin : doCad}>
          {tab === 'login' ? 'Entrar' : 'Criar conta'}
        </button>
      </div>
    </Overlay>
  );
}

export default AuthOverlay;