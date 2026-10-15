const AVATARS=['🦊','🧙','🐉','🎭','👾','🦸','🕵️','🤖'];
const COLORS=['#c9963a','#d07060','#6dba8a','#9fcfdb'];
const STATES=[
  {id:'AM',name:'Amazonas',reg:'Norte',tc:'#6dba8a'},
  {id:'PA',name:'Pará',reg:'Norte',tc:'#6dba8a'},
  {id:'TO',name:'Tocantins',reg:'Norte',tc:'#6dba8a'},
  {id:'AC',name:'Acre',reg:'Norte',tc:'#6dba8a'},
  {id:'RO',name:'Rondônia',reg:'Norte',tc:'#6dba8a'},
  {id:'MA',name:'Maranhão',reg:'Nordeste',tc:'#f0a090'},
  {id:'PI',name:'Piauí',reg:'Nordeste',tc:'#f0a090'},
  {id:'CE',name:'Ceará',reg:'Nordeste',tc:'#f0a090'},
  {id:'PE',name:'Pernambuco',reg:'Nordeste',tc:'#f0a090'},
  {id:'BA',name:'Bahia',reg:'Nordeste',tc:'#f0a090'},
  {id:'AL',name:'Alagoas',reg:'Nordeste',tc:'#f0a090'},
  {id:'MT',name:'Mato Grosso',reg:'Centro-Oeste',tc:'#9fcfdb'},
  {id:'GO',name:'Goiás',reg:'Centro-Oeste',tc:'#9fcfdb'},
  {id:'MS',name:'Mato Grosso do Sul',reg:'Centro-Oeste',tc:'#9fcfdb'},
  {id:'DF',name:'Distrito Federal',reg:'Centro-Oeste',tc:'#c0b0f0'},
  {id:'MG',name:'Minas Gerais',reg:'Sudeste',tc:'#f0a080'},
  {id:'SP',name:'São Paulo',reg:'Sudeste',tc:'#f0a080'},
  {id:'RJ',name:'Rio de Janeiro',reg:'Sudeste',tc:'#f0a080'},
  {id:'PR',name:'Paraná',reg:'Sul',tc:'#a0b0e0'},
  {id:'SC',name:'Santa Catarina',reg:'Sul',tc:'#a0b0e0'},
];
const MISSIONS=[
  {id:0,text:'Controle todos os estados do Sudeste e 2 do Centro-Oeste',check:(t,me)=>{const sud=STATES.filter(s=>s.reg==='Sudeste').map(s=>s.id);const co=STATES.filter(s=>s.reg==='Centro-Oeste').map(s=>s.id);return sud.every(id=>t[id]===me)&&co.filter(id=>t[id]===me).length>=2;}},
  {id:1,text:'Domine 8 estados nas regiões Norte e Nordeste',check:(t,me)=>{const ids=STATES.filter(s=>s.reg==='Norte'||s.reg==='Nordeste').map(s=>s.id);return ids.filter(id=>t[id]===me).length>=8;}},
  {id:2,text:'Controle o Centro-Oeste completo incluindo o Distrito Federal',check:(t,me)=>{const ids=STATES.filter(s=>s.reg==='Centro-Oeste').map(s=>s.id);return ids.every(id=>t[id]===me);}},
  {id:3,text:'Tenha ao menos 12 estados sob controle simultâneo',check:(t,me)=>Object.values(t).filter(v=>v===me).length>=12},
];
const QS=[
  {q:'O Senado Federal é composto por 3 senadores por estado, totalizando 81 senadores?',c:true,exp:'Correto! O Senado representa os estados com igualdade: 3 senadores por unidade federativa × 27 = 81 senadores no total, com mandatos de 8 anos.'},
  {q:'A Câmara dos Deputados possui 513 deputados federais eleitos proporcionalmente?',c:true,exp:'Isso mesmo! São 513 deputados federais, eleitos pelo sistema proporcional por estado. Cada estado tem um mínimo de 8 e máximo de 70 deputados.'},
  {q:'O princípio federativo na CF/88 concentra todo o poder no governo federal?',c:false,exp:'Errado! O federalismo divide o poder entre União, estados e municípios, garantindo autonomia a cada ente. É o oposto da centralização.'},
  {q:'O TCU (Tribunal de Contas da União) tem função de julgar crimes cometidos por políticos?',c:false,exp:'Não! O TCU fiscaliza o uso dos recursos públicos federais — é um órgão de controle externo, não um tribunal criminal. Crimes são julgados pela Justiça.'},
  {q:'O mandato de um senador no Brasil dura 8 anos, com renovações alternadas de 1/3 e 2/3?',c:true,exp:'Correto! O mandato senatorial é de 8 anos. A renovação ocorre de 4 em 4 anos, alternando 1/3 e 2/3 das cadeiras para garantir continuidade.'},
  {q:'O filibuster é uma técnica legislativa que consiste em obstruir votações com discursos prolongados?',c:true,exp:'Exato! O filibuster é a prática de usar o direito à palavra sem limite de tempo para atrasar ou impedir votações — comum no Senado americano.'},
  {q:'"Recall" político significa a revogação do mandato de um representante eleito pelos próprios eleitores?',c:true,exp:'Correto! O recall é um mecanismo de democracia direta que permite aos cidadãos destituir um político antes do fim do mandato por meio de votação.'},
  {q:'No Brasil, toda proposta de lei obrigatoriamente começa no Senado Federal?',c:false,exp:'Errado! O processo legislativo ordinário geralmente começa na Câmara dos Deputados. O Senado atua como câmara revisora na maioria dos casos.'},
  {q:'O voto é obrigatório no Brasil para todos os cidadãos, incluindo maiores de 70 anos?',c:false,exp:'Incorreto! O voto é facultativo para maiores de 70 anos (e também para analfabetos e jovens entre 16 e 18 anos). É obrigatório dos 18 aos 70 anos.'},
  {q:'O Brasil possui um sistema presidencialista de governo, onde o presidente acumula funções de chefe de Estado e de governo?',c:true,exp:'Correto! No presidencialismo brasileiro, o Presidente da República é simultaneamente chefe de Estado (representa o país) e chefe de governo (dirige a administração).'},
];
const MAP_POS={
  AM:{x:32,y:24,w:52,h:38},PA:{x:90,y:22,w:46,h:34},TO:{x:138,y:18,w:34,h:28},
  AC:{x:18,y:66,w:38,h:27},RO:{x:58,y:65,w:40,h:27},
  MA:{x:178,y:18,w:34,h:25},PI:{x:215,y:16,w:30,h:24},CE:{x:215,y:44,w:30,h:23},
  PE:{x:215,y:71,w:30,h:22},BA:{x:176,y:49,w:36,h:32},AL:{x:248,y:16,w:28,h:22},
  MT:{x:108,y:57,w:50,h:38},GO:{x:162,y:58,w:42,h:31},MS:{x:62,y:98,w:44,h:32},
  DF:{x:157,y:93,w:28,h:22},
  MG:{x:175,y:104,w:40,h:32},SP:{x:185,y:140,w:46,h:32},RJ:{x:221,y:107,w:34,h:25},
  PR:{x:142,y:147,w:37,h:27},SC:{x:142,y:177,w:37,h:26},
};

function shuffle(a){const r=[...a];for(let i=r.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[r[i],r[j]]=[r[j],r[i]];}return r;}

export {
  AVATARS,
  COLORS,
  STATES,
  MISSIONS,
  QS,
  MAP_POS,
  shuffle
};
